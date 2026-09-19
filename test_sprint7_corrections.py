from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import Mock, patch

from app.services import enrichment_service as enrichment
from app.services.gap_analyzer_service import analyze_gaps
from app.services.opportunity.opportunity_score import calculate_opportunity_score
from app.services.opportunity.diagnosis_engine import build_diagnosis

with patch("groq.Groq"):
    from app.services import agency_report_service as report
    from app.services import groq_service as analysis


class Sprint7CorrectionsTests(unittest.TestCase):
    def setUp(self):
        network = patch("requests.sessions.Session.request",
                        side_effect=AssertionError("HTTP real proibido"))
        network.start()
        self.addCleanup(network.stop)
        output = redirect_stdout(StringIO())
        output.__enter__()
        self.addCleanup(output.__exit__, None, None, None)

    def enrich(self, website, html):
        lead = {"website": website, "digital_maturity_score": 0}
        with patch.object(enrichment, "fetch_html", return_value=html), \
             patch.object(enrichment, "find_internal_pages", return_value=[]), \
             patch.object(enrichment, "extract_social_links", return_value={}), \
             patch.object(enrichment, "extract_contacts", return_value={}), \
             patch.object(enrichment, "extract_structured_data", return_value={}):
            enrichment.enrich_lead(lead)
        return lead

    def test_three_audit_states_and_zero_maturity(self):
        unavailable = self.enrich("http://example.com", None)
        completed = self.enrich("http://example.com", "<html></html>")
        missing = self.enrich(None, None)
        self.assertEqual(unavailable["website_audit_status"], "unavailable")
        self.assertEqual(completed["website_audit_status"], "completed")
        self.assertEqual(missing["website_audit_status"], "no_site")
        for lead in (unavailable, completed, missing):
            self.assertEqual(lead["digital_maturity_score"], 0)
            analyze_gaps(lead)
        self.assertEqual(unavailable["website_gaps"], [])
        self.assertIn("Auditoria do website indisponível", build_diagnosis(unavailable, 25))
        self.assertIn("form", completed["website_gaps"])
        self.assertEqual(missing["website_gaps"], ["website_missing"])
        # O estado não muda a fórmula de oportunidade.
        for lead in (unavailable, completed):
            calculate_opportunity_score(lead)
        self.assertEqual(unavailable["opportunity_score"], completed["opportunity_score"])
        self.assertEqual(unavailable["website_opportunity_score"], 90)

    def test_unavailable_audit_cannot_generate_specific_claims(self):
        lead = self.enrich("http://example.com", None)
        lead.update({"prioridade": "Baixa", "confidence": 25,
                     "problema_principal": "Site sem formulário"})
        with patch.object(analysis, "client") as ai, patch.object(report, "client") as writer:
            analysis.analyze_lead(lead)
            report.generate_agency_report(lead)
            ai.chat.completions.create.assert_not_called()
            writer.chat.completions.create.assert_not_called()
        text = lead["resumo_comercial"] + lead["motivo_indicacao"] + lead["problema_principal"]
        self.assertIn("indisponível", text)
        self.assertNotIn("sem formulário", text)
        self.assertNotIn("presença digital consolidada", text)

    def test_low_priority_prompt_uses_evidence_not_assumptions(self):
        lead = {"empresa": "Exemplo", "prioridade": "Baixa", "confidence": 0,
                "website_audit_status": "no_site", "tem_site": False,
                "website_opportunities": ["Empresa sem site próprio identificado"]}
        response = Mock()
        response.choices = [Mock(message=Mock(content='{"resumo_comercial": "Website não identificado.", "motivo_indicacao": "Validar presença digital."}'))]
        with patch.object(report, "client") as client:
            client.chat.completions.create.return_value = response
            report.generate_agency_report(lead)
            prompt = client.chat.completions.create.call_args.kwargs["messages"][0]["content"]
        self.assertNotIn("informe claramente que a empresa possui", prompt)
        self.assertIn("não comprovam presença digital consolidada", prompt)
        self.assertIn("Ausência de evidência não comprova ausência real", prompt)
        self.assertIn("Confiança: 0", prompt)
        self.assertIn("Empresa sem site próprio identificado", prompt)
        self.assertNotIn("presença digital consolidada", lead["resumo_comercial"])


if __name__ == "__main__":
    unittest.main()
