import unittest

from app.services.fit.fit_score import calculate_fit_score, normalize_segment_text
from app.services.opportunity.category_weight import category_weight


class FitScoreTests(unittest.TestCase):
    def test_traditional_segments(self):
        for category in ("Clínica especializada", "Consultoria", "Dentista"):
            with self.subTest(category=category):
                lead = {"categoria": category, "empresa": "Qualquer nome"}
                calculate_fit_score(lead)
                self.assertEqual(lead["fit_score"], 30)

    def test_approved_fallbacks(self):
        for category, name in (
            ("Centro de saúde e beleza", "Clínica Estética Virtuosa"),
            ("Centro de saúde e beleza", "Dra. Dyane Cristini Biomedicina Estética"),
            ("Centro de saúde e beleza", "Pró-Corpo Estética Avançada"),
            ("Esteticista", "Empresa Estética Avançada"),
            ("Esteticista", "Clínica de Estética Exemplo"),
        ):
            with self.subTest(name=name):
                lead = {"categoria": category, "empresa": name}
                calculate_fit_score(lead)
                self.assertEqual(lead["fit_score"], 30)
                self.assertEqual(lead["categoria"], category)
                self.assertEqual(lead["empresa"], name)
                self.assertEqual(category_weight(lead), 0)

    def test_normalization(self):
        self.assertEqual(normalize_segment_text("  CLÍNICA\tESTÉTICA\n"), "clinica estetica")
        self.assertEqual(normalize_segment_text(None), "")
        lead = {"categoria": " CENTRO DE SAÚDE   E BELEZA ",
                "empresa": "CLI\u0301NICA\tESTE\u0301TICA Virtuosa"}
        calculate_fit_score(lead)
        self.assertEqual(lead["fit_score"], 30)

    def test_generic_names_and_ineligible_categories(self):
        for category, name in (
            ("Centro de saúde e beleza", "Spa Nature"),
            ("Centro de saúde e beleza", "Vous Estética São Bernardo"),
            ("Centro de saúde e beleza", "Pró Estética"),
            ("Esteticista", "Salão Beleza"),
            ("Salão de beleza", "Empresa Estética Avançada"),
            ("Centro de saúde e beleza e spa", "Clínica Estética"),
            (None, "Clínica Estética"),
            ("Esteticista", None),
        ):
            with self.subTest(category=category, name=name):
                lead = {"categoria": category, "empresa": name}
                calculate_fit_score(lead)
                self.assertEqual(lead["fit_score"], 0)

    def test_phrase_boundaries(self):
        for name in ("Superclinica estetica", "Estetica avancadissima",
                     "Biomedicina esteticamente", "Clinica esteticas"):
            with self.subTest(name=name):
                lead = {"categoria": "Esteticista", "empresa": name}
                calculate_fit_score(lead)
                self.assertEqual(lead["fit_score"], 0)

    def test_existing_review_thresholds(self):
        for reviews, points in ((19, 0), (20, 10), (49, 10), (50, 20),
                                (99, 20), (100, 25), (199, 25), (200, 30)):
            lead = {"categoria": "Clínica", "reviews": reviews}
            calculate_fit_score(lead)
            self.assertEqual(lead["fit_score"], 30 + points)

    def test_existing_reputation_thresholds(self):
        for rating, points in ((3.4, 0), (3.5, 5), (3.9, 5), (4, 15),
                               (4.4, 15), (4.5, 20), (5, 20)):
            lead = {"categoria": "Clínica", "avaliacao": rating}
            calculate_fit_score(lead)
            self.assertEqual(lead["fit_score"], 30 + points)

    def test_contact_structure_and_caps_unchanged(self):
        for field in ("telefone", "tem_email", "tem_whatsapp", "tem_site", "tem_instagram"):
            lead = {"categoria": "Clínica", field: True}
            calculate_fit_score(lead)
            self.assertEqual(lead["fit_score"], 40)
        base = {"reviews": 500, "avaliacao": 5, "telefone": "telefone",
                "tem_email": True, "tem_whatsapp": True, "tem_site": True,
                "tem_instagram": True}
        for category, name, expected in (
            ("Clínica", "Estética Avançada", 100),
            ("Esteticista", "Estética Avançada", 100),
            ("Esteticista", "Spa Nature", 50),
        ):
            lead = dict(base, categoria=category, empresa=name)
            calculate_fit_score(lead)
            self.assertEqual(lead["fit_score"], expected)


if __name__ == "__main__":
    unittest.main()
