from dataclasses import dataclass


@dataclass
class LeadModel:

    empresa: str = None
    categoria: str = None

    cidade: str = None
    estado: str = None

    telefone: str = None

    website: str = None
    instagram: str = None
    email: str = None

    avaliacao: float = 0
    reviews: int = 0

    tem_site: bool = False
    tem_whatsapp: bool = False
    tem_instagram: bool = False
    tem_email: bool = False

    score: int = 0

    score_oportunidade: int = 0

    problema_principal: str = None
    abordagem: str = None

    servico_recomendado: str = None
    prioridade: str = None

    resumo_comercial: str = None
    motivo_indicacao: str = None

    qualificado: bool = False