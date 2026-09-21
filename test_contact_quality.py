from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from app.services.enrichment.email_validator import validate_email
from app.services.enrichment.contact_extractor import extract_contacts
from app.services.enrichment.structured_data import extract_structured_data
from app.services import enrichment_service as enrichment


class ContactQualityTests(unittest.TestCase):
    def setUp(self):
        output = redirect_stdout(StringIO())
        output.__enter__()
        self.addCleanup(output.__exit__, None, None, None)
        network = patch("requests.sessions.Session.request",
                        side_effect=AssertionError("HTTP real proibido"))
        network.start()
        self.addCleanup(network.stop)

    def test_exact_placeholders_rejected(self):
        for email in ("johndoe@domain.com", "joao@dominio.com.br",
                      " JOHNDOE@DOMAIN.COM "):
            self.assertFalse(validate_email(email))

    def test_legitimate_emails_unchanged(self):
        for email in ("contato@onodera.com.br", "contato@loja.onodera.com.br",
                      "sacproestetica@gmail.com", "joao@empresa.com.br",
                      "contato@dominio.com.br", "vendas@domain.com"):
            self.assertTrue(validate_email(email))
            self.assertEqual(extract_contacts(email)["email"], email)

    def test_placeholder_does_not_hide_next_valid_email(self):
        result = extract_contacts("johndoe@domain.com joao@dominio.com.br contato@onodera.com.br")
        self.assertEqual(result["email"], "contato@onodera.com.br")
        self.assertEqual(result["email_score"], 100)

    def test_loose_numbers_rejected_by_both_extractors(self):
        html = '<script>var id = 1788874275;</script><p>1788874275</p><div data-id="11999121430">33425280</div>'
        self.assertIsNone(extract_contacts(html)["telefone"])
        self.assertIsNone(extract_structured_data(html)["telefone"])

    def test_tel_link_preserves_normalization(self):
        for href in ("tel:+5511999121430", "TEL:+5511999121430"):
            result = extract_contacts(f'<a href="{href}">Ligar</a>')
            self.assertEqual(result["telefone"], "(11) 99912-1430")

    def test_jsonld_telephone_and_contact_point(self):
        for data in ('{"telephone":"+5511999121430"}',
                     '{"contactPoint":{"telephone":"+5511999121430"}}'):
            html = f'<script type="application/ld+json">{data}</script>'
            self.assertEqual(extract_structured_data(html)["telefone"], "(11) 99912-1430")

    def test_enrichment_sources_and_maps_priority(self):
        for html, expected in (
            ('<p>1788874275</p>', None),
            ('<a href="tel:+5511999121430">Ligar</a>', "(11) 99912-1430"),
            ('<p>1788874275</p><script type="application/ld+json">'
             '{"telephone":"+5511999121430"}</script>', "(11) 99912-1430"),
        ):
            for original in (None, "+55 11 3342-5280"):
                with self.subTest(html=html, original=original):
                    lead = {"website": "https://onodera.com.br", "telefone": original}
                    with patch.object(enrichment, "fetch_html", return_value=html), \
                         patch.object(enrichment, "find_internal_pages", return_value=[]):
                        enrichment.enrich_lead(lead)
                    self.assertEqual(lead["telefone"], original or expected)

    def test_whatsapp_detection_unchanged(self):
        result = extract_contacts('<a href="https://wa.me/5511999121430">Contato</a>')
        self.assertTrue(result["tem_whatsapp"])
        self.assertIsNone(result["telefone"])


if __name__ == "__main__":
    unittest.main()
