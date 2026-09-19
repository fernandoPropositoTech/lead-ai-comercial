from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import Mock, patch

# Evita inicializar clientes externos ao importar a orquestração.
with patch.dict("sys.modules", {
    name: Mock() for name in (
        "app.services.groq_service", "app.services.agency_report_service",
        "app.services.supabase_service", "app.services.csv_service",
    )
}):
    from app import main as pipeline

from app.processors.lead_processor import process_leads
from app.services import enrichment_service as enrichment


class InstagramIntegrationTests(unittest.TestCase):
    def setUp(self):
        network = patch("requests.sessions.Session.request",
                        side_effect=AssertionError("HTTP real proibido"))
        network.start()
        self.addCleanup(network.stop)
        output = redirect_stdout(StringIO())
        output.__enter__()
        self.addCleanup(output.__exit__, None, None, None)
        collector = patch.object(pipeline, "collect_instagram_data")
        self.collect = collector.start()
        self.addCleanup(collector.stop)
        self.collect.return_value = {
            "profile": {"followersCount": 3000, "postsCount": 80}, "posts": [],
        }
        self.url = "https://www.instagram.com/exemplo/"

    def test_with_and_without_website(self):
        for website in (None, "https://example.com"):
            with self.subTest(website=website):
                lead = {"instagram": self.url, "website": website}
                with patch.object(pipeline, "extract_instagram_metrics",
                                  wraps=pipeline.extract_instagram_metrics) as extract, \
                     patch.object(pipeline, "calculate_instagram_score",
                                  wraps=pipeline.calculate_instagram_score) as score:
                    self.assertIs(pipeline.enrich_instagram_leads([lead])[0], lead)
                    extract.assert_called_once_with(self.collect.return_value["profile"], [])
                    score.assert_called_once_with(lead)
                self.assertEqual(lead["instagram_score"], 45)
                self.assertFalse(lead["instagram_active"])
                self.assertTrue(lead["instagram_data_available"])
                self.assertTrue(lead["tem_instagram"])

    def test_raw_website_instagram_and_normal_website(self):
        leads = process_leads([
            {"website": self.url}, {"website": "https://example.com"},
            {"website": "https://instagram.com/p/abc/"}, {},
        ])
        self.assertEqual(leads[0]["instagram"], self.url)
        self.assertTrue(leads[0]["tem_instagram"])
        self.assertIsNone(leads[0]["website"])
        self.assertEqual(leads[1]["website"], "https://example.com")
        for lead in leads[1:]:
            self.assertIsNone(lead["instagram"])
            self.assertFalse(lead["tem_instagram"])

    def test_enrichment_preserves_existing_and_discovers_fallback(self):
        for existing in (self.url, None):
            with self.subTest(existing=existing):
                lead = {"website": "https://example.com", "instagram": existing}
                discovered = None if existing else self.url
                with patch.object(enrichment, "fetch_html", return_value="<html></html>"), \
                     patch.object(enrichment, "find_internal_pages", return_value=[]), \
                     patch.object(enrichment, "extract_social_links", return_value={"instagram": discovered}), \
                     patch.object(enrichment, "extract_contacts", return_value={}), \
                     patch.object(enrichment, "extract_structured_data", return_value={}):
                    enrichment.enrich_lead(lead)
                self.assertEqual(lead["instagram"], self.url)
                self.assertTrue(lead["tem_instagram"])

    def test_early_returns_do_not_prevent_instagram(self):
        for website in (None, "https://example.com"):
            lead = {"website": website, "instagram": self.url}
            with patch.object(enrichment, "fetch_html", return_value=None):
                enrichment.enrich_lead(lead)
            pipeline.enrich_instagram_leads([lead])
            self.assertEqual(lead["instagram_score"], 45)

    def test_absent_or_invalid_instagram(self):
        for url in (None, "https://example.com", "https://instagram.com/p/abc/"):
            lead = {"instagram": url, "instagram_score": 100, "instagram_active": True}
            pipeline.enrich_instagram_leads([lead])
            self.assertFalse(lead["instagram_data_available"])
            self.assertEqual(lead["instagram_score"], 0)
            self.assertIsNone(lead["instagram_active"])
        self.collect.assert_not_called()

    def test_normalized_cache(self):
        leads = [{"instagram": url} for url in (
            self.url, "http://instagram.com/EXEMPLO?source=test",
        )]
        pipeline.enrich_instagram_leads(leads)
        self.collect.assert_called_once_with(self.url)
        self.assertEqual([lead["instagram_score"] for lead in leads], [45, 45])

    def test_empty_result_cached_and_presence_preserved(self):
        self.collect.return_value = {"profile": None, "posts": []}
        leads = [{"instagram": self.url, "tem_instagram": True} for _ in range(2)]
        pipeline.enrich_instagram_leads(leads)
        self.collect.assert_called_once()
        for lead in leads:
            self.assertEqual(lead["instagram"], self.url)
            self.assertTrue(lead["tem_instagram"])
            self.assertFalse(lead["instagram_data_available"])
            self.assertEqual(lead["instagram_score"], 0)
            self.assertIsNone(lead["instagram_active"])

    def test_exception_cached_and_next_profile_processed(self):
        self.collect.side_effect = [RuntimeError("simulado"), self.collect.return_value]
        leads = [{"instagram": url} for url in (self.url, self.url, "https://instagram.com/outro/")]
        pipeline.enrich_instagram_leads(leads)
        self.assertEqual(self.collect.call_count, 2)
        self.assertTrue(leads[0]["tem_instagram"])
        self.assertEqual(leads[0]["instagram"], self.url)
        self.assertEqual([lead["instagram_score"] for lead in leads], [0, 0, 45])

    def test_main_stage_order_and_continuation(self):
        lead = {"instagram": self.url}
        self.collect.side_effect = RuntimeError("simulado")
        events = []
        def website_stage(leads):
            events.append("website")
            return leads
        def instagram_stage(leads):
            events.append("instagram")
            return pipeline.enrich_instagram_leads_original(leads)
        def scoring_stage(leads):
            events.append("scoring")
            self.assertEqual(leads[0]["instagram_score"], 0)
            return leads
        with patch.object(pipeline, "search_businesses", return_value=[{}]), \
             patch.object(pipeline, "process_leads", return_value=[lead]), \
             patch.object(pipeline, "enrich_leads", side_effect=website_stage), \
             patch.object(pipeline, "enrich_instagram_leads_original", pipeline.enrich_instagram_leads, create=True), \
             patch.object(pipeline, "enrich_instagram_leads", side_effect=instagram_stage), \
             patch.object(pipeline, "score_leads", side_effect=scoring_stage), \
             patch.object(pipeline, "calculate_fit_score"), \
             patch.object(pipeline, "calculate_opportunity"), \
             patch.object(pipeline, "analyze_gaps"), \
             patch.object(pipeline, "recommend_service"), \
             patch.object(pipeline, "qualify_lead"), \
             patch.object(pipeline, "save_leads") as save:
            pipeline.main()
            save.assert_called_once_with([lead])
        self.assertEqual(events, ["website", "instagram", "scoring"])


if __name__ == "__main__":
    unittest.main()
