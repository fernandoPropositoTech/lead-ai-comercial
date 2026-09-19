from datetime import datetime, timezone

from app.services.instagram_intelligence_service import (
    calculate_instagram_score,
    extract_instagram_metrics,
)


cenarios = [
    {
        "nome": "A - Perfil forte e ativo",
        "instagram_data_available": True,
        "instagram_followers": 12000,
        "instagram_posts_count": 180,
        "instagram_last_post_days": 3,
    },
    {
        "nome": "B - Perfil médio e ativo",
        "instagram_data_available": True,
        "instagram_followers": 1800,
        "instagram_posts_count": 45,
        "instagram_last_post_days": 10,
    },
    {
        "nome": "C - Perfil grande e inativo",
        "instagram_data_available": True,
        "instagram_followers": 15000,
        "instagram_posts_count": 220,
        "instagram_last_post_days": 120,
    },
    {
        "nome": "D - Dados indisponíveis",
        "instagram_data_available": False,
        "instagram_followers": None,
        "instagram_posts_count": None,
        "instagram_last_post_days": None,
    },
    {
        "nome": "E - Dados disponíveis, mas recência desconhecida",
        "instagram_data_available": True,
        "instagram_followers": 3000,
        "instagram_posts_count": 80,
        "instagram_last_post_days": None,
    },
]


resultados_esperados = [
    (100, True),
    (70, True),
    (60, False),
    (0, None),
    (45, False),
]


for lead, (score_esperado, ativo_esperado) in zip(
    cenarios, resultados_esperados
):

    calculate_instagram_score(
        lead
    )

    assert lead["instagram_score"] == score_esperado, (
        f"{lead['nome']}: score esperado {score_esperado}, "
        f"obtido {lead['instagram_score']}"
    )
    assert lead["instagram_active"] is ativo_esperado, (
        f"{lead['nome']}: ativo esperado {ativo_esperado}, "
        f"obtido {lead.get('instagram_active')}"
    )

    print(
        f"\n{lead['nome']}"
    )

    print(
        f"Score: "
        f"{lead['instagram_score']}/100"
    )

    print(
        f"Ativo: "
        f"{lead.get('instagram_active')}"
    )


reference = datetime(2025, 10, 20, 12, tzinfo=timezone.utc)
profile = {"username": "exemplo", "followersCount": 3000, "postsCount": 80}
posts = [
    {"timestamp": "2025-10-18T00:00:00.000Z"},
    {"timestamp": "2025-10-10T00:00:00.000Z"},
    {"timestamp": "2025-10-13T12:00:00.000Z"},
]
metrics = extract_instagram_metrics(profile, posts, reference)
assert metrics["instagram_followers"] == 3000
assert metrics["instagram_posts_count"] == 80
assert metrics["instagram_last_post_days"] == 2
assert metrics["instagram_posting_frequency_days"] == 4.0
assert metrics["instagram_data_available"] is True

# Comentários recentes não afetam recência nem frequência.
posts_with_comments = [
    {
        **post,
        "latestComments": [{"timestamp": "2025-10-20T11:59:00.000Z"}],
    }
    for post in posts
]
assert extract_instagram_metrics(profile, posts_with_comments, reference) == metrics

# Timestamps inválidos, campos ausentes e itens inválidos são ignorados.
invalid_posts = [
    {"timestamp": "invalido"},
    {"timestamp": "2025-02-30T00:00:00Z"},
    {"timestamp": None},
    {"timestamp": 123},
    {"latestComments": [{"timestamp": "2025-10-20T11:59:00Z"}]},
    None,
]
assert extract_instagram_metrics(profile, posts + invalid_posts, reference) == metrics
unknown = extract_instagram_metrics(profile, invalid_posts, reference)
assert unknown["instagram_last_post_days"] is None
assert unknown["instagram_posting_frequency_days"] is None
assert unknown["instagram_data_available"] is True
calculate_instagram_score(unknown)
assert unknown["instagram_score"] == 45
assert unknown["instagram_active"] is False

single = extract_instagram_metrics(profile, posts[:1], reference)
assert single["instagram_last_post_days"] == 2
assert single["instagram_posting_frequency_days"] is None

empty = extract_instagram_metrics(None, None, reference)
assert empty == {
    "instagram_followers": None,
    "instagram_posts_count": None,
    "instagram_last_post_days": None,
    "instagram_posting_frequency_days": None,
    "instagram_data_available": False,
}
assert extract_instagram_metrics({}, [], reference) == empty
partial = extract_instagram_metrics(None, posts, reference)
assert partial["instagram_followers"] is None
assert partial["instagram_posts_count"] is None
assert partial["instagram_last_post_days"] == 2
assert partial["instagram_posting_frequency_days"] == 4.0
assert partial["instagram_data_available"] is True

print("\nTransformação Apify: todas as assertions passaram.")
