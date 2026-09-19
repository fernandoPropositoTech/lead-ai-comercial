from datetime import datetime, timezone


def extract_instagram_metrics(profile_data, posts, reference_datetime=None):
    """Retorna métricas sem modificar as entradas; datas sem fuso usam UTC."""
    reference = reference_datetime or datetime.now(timezone.utc)
    if reference.tzinfo is None:
        reference = reference.replace(tzinfo=timezone.utc)
    reference = reference.astimezone(timezone.utc)

    profile = profile_data if isinstance(profile_data, dict) else {}

    def count_value(key):
        value = profile.get(key)
        return value if type(value) is int and value >= 0 else None

    timestamps = []
    for post in posts or []:
        if not isinstance(post, dict):
            continue
        raw_timestamp = post.get("timestamp")
        if not isinstance(raw_timestamp, str):
            continue
        try:
            timestamp = datetime.fromisoformat(
                raw_timestamp.replace("Z", "+00:00")
            )
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            timestamps.append(timestamp.astimezone(timezone.utc))
        except (ValueError, OverflowError):
            continue

    timestamps.sort()
    frequency = None
    if len(timestamps) >= 2:
        intervals = [
            (current - previous).total_seconds() / 86400
            for previous, current in zip(timestamps, timestamps[1:])
        ]
        frequency = sum(intervals) / len(intervals)

    followers = count_value("followersCount")
    posts_count = count_value("postsCount")
    return {
        "instagram_followers": followers,
        "instagram_posts_count": posts_count,
        "instagram_last_post_days": (
            max(0, (reference - timestamps[-1]).days) if timestamps else None
        ),
        "instagram_posting_frequency_days": frequency,
        "instagram_data_available": (
            followers is not None or posts_count is not None or bool(timestamps)
        ),
    }


def calculate_instagram_score(lead):

    # ----------------------------------
    # VERIFICAÇÃO DE DADOS
    # ----------------------------------

    data_available = lead.get(
        "instagram_data_available",
        False
    )

    if not data_available:

        lead["instagram_score"] = 0
        lead["instagram_active"] = None
        return lead

    followers = lead.get(
        "instagram_followers"
    )

    posts_count = lead.get(
        "instagram_posts_count"
    )

    last_post_days = lead.get(
        "instagram_last_post_days"
    )

    # ----------------------------------
    # 1. AUDIÊNCIA
    # Máximo: 40 pontos
    # ----------------------------------

    followers_score = 0

    if followers is not None:

        if followers >= 10000:
            followers_score = 40

        elif followers >= 5000:
            followers_score = 35

        elif followers >= 2000:
            followers_score = 30

        elif followers >= 1000:
            followers_score = 25

        elif followers >= 500:
            followers_score = 20

        elif followers >= 100:
            followers_score = 10

    # ----------------------------------
    # 2. ATIVIDADE / RECÊNCIA
    # Máximo: 40 pontos
    # ----------------------------------

    activity_score = 0

    if last_post_days is not None:

        if last_post_days <= 7:
            activity_score = 40

        elif last_post_days <= 14:
            activity_score = 35

        elif last_post_days <= 30:
            activity_score = 25

        elif last_post_days <= 60:
            activity_score = 15

        elif last_post_days <= 90:
            activity_score = 5

    # ----------------------------------
    # 3. HISTÓRICO DE CONTEÚDO
    # Máximo: 20 pontos
    # ----------------------------------

    posts_score = 0

    if posts_count is not None:

        if posts_count >= 100:
            posts_score = 20

        elif posts_count >= 50:
            posts_score = 15

        elif posts_count >= 20:
            posts_score = 10

        elif posts_count >= 5:
            posts_score = 5

    # ----------------------------------
    # SCORE FINAL
    # ----------------------------------

    score = (
        followers_score
        + activity_score
        + posts_score
    )

    score = max(
        0,
        min(score, 100)
    )

    lead["instagram_score"] = score

    # ----------------------------------
    # PERFIL ATIVO
    # ----------------------------------

    lead["instagram_active"] = (
        last_post_days is not None
        and last_post_days <= 30
    )

    return lead
