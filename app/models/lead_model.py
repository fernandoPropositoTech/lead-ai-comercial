class LeadModel:

    @staticmethod
    def create():

        return {

            # Dados básicos
            "empresa": None,
            "categoria": None,
            "cidade": None,
            "estado": None,
            "telefone": None,
            "website": None,
            "instagram": None,
            "email": None,

            # Google
            "avaliacao": 0,
            "reviews": 0,

            # Presença digital
            "tem_site": False,
            "tem_whatsapp": False,
            "tem_instagram": False,
            "tem_email": False,

            # Enriquecimento
            "html": None,
            "trafego_pago": False,

            # Scores
            "score": 0,
            "score_digital": 0,
            "score_comercial": 0,
            "score_final": 0,
            "score_oportunidade": 0,
            "digital_maturity_score": 0,

            # Digital Maturity
            "digital_scores": {},
            "gaps": [],
            "gap_priorities": {},

            # Recomendação
            "servico_recomendado": None,
            "prioridade": None,

            # IA
            "problema_principal": None,
            "abordagem": None,
            "resumo_comercial": None,
            "motivo_indicacao": None,

            # Ranking
            "ranking_comercial": None,

            # Qualificação
            "qualificado": False
        }