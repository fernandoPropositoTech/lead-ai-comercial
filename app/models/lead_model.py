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

    # ----------------------------------
    # SCORES BASE
    # ----------------------------------

    score: int = 0
    website_score: int = 0
    email_score: int = 0
    score_digital: int = 0
    score_comercial: int = 0
    ranking_comercial: int = 0

    # ----------------------------------
    # FIT COMERCIAL - SPRINT 4
    # ----------------------------------

    fit_score: int = 0

    # ----------------------------------
    # WEBSITE INTELLIGENCE - SPRINT 5
    # ----------------------------------

    digital_maturity_score: int = 0

    digital_scores: dict = field(
        default_factory=dict
    )

    website_audit: dict = field(
        default_factory=dict
    )

    website_gaps: list = field(
        default_factory=list
    )

    website_opportunities: list = field(
        default_factory=list
    )

    website_opportunity_score: int = 0

    # ----------------------------------
    # INSTAGRAM INTELLIGENCE - SPRINT 6
    # ----------------------------------

    instagram_followers: int | None = None
    instagram_posts_count: int | None = None
    instagram_last_post_days: int | None = None
    instagram_posting_frequency_days: float | None = None
    instagram_active: bool | None = None
    instagram_score: int = 0
    instagram_data_available: bool = False

    # ----------------------------------
    # OPORTUNIDADE
    # ----------------------------------

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
