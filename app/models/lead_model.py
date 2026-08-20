from dataclasses import dataclass, field


@dataclass
class LeadModel:

    empresa: str = None
    categoria: str = None

    cidade: str = None
    estado: str = None

    telefone: str = None

    website: str = None
    instagram: str = None
    facebook: str = None
    linkedin: str = None
    youtube: str = None
    tiktok: str = None

    email: str = None

    avaliacao: float = 0
    reviews: int = 0

    tem_site: bool = False
    tem_whatsapp: bool = False
    tem_instagram: bool = False
    tem_email: bool = False

    score: int = 0

    website_score: int = 0
    email_score: int = 0

    score_digital: int = 0
    score_comercial: int = 0
    ranking_comercial: int = 0

    opportunity_score: int = 0
    confidence: int = 0

    problema_principal: str = None
    abordagem: str = None

    servico_recomendado: str = None
    prioridade: str = None

    resumo_comercial: str = None
    motivo_indicacao: str = None

    qualificado: bool = False

    diagnostico: list = field(
        default_factory=list
    )

    opportunity_explanation: str = None