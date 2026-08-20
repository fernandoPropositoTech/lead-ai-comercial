import re

from app.services.enrichment.email_validator import (
    validate_email
)

from app.services.enrichment.email_score import (
    calculate_email_score
)


EMAIL_PATTERN = (
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)


PHONE_PATTERN = (
    r"(?:\+55\s?)?"
    r"(?:\(?\d{2}\)?\s?)?"
    r"\d{4,5}[-\s]?\d{4}"
)


WHATSAPP_PATTERNS = [

    r"https?://wa\.me/\d+",

    r"https?://api\.whatsapp\.com/send\?phone=\d+",

    r"https?://web\.whatsapp\.com",

    r"whatsapp"

]


def normalize_phone(phone):

    if not phone:
        return None

    # Remove tudo que não for número
    digits = re.sub(
        r"\D",
        "",
        phone
    )

    # Remove código do Brasil quando realmente estiver presente
    if digits.startswith("55") and len(digits) > 11:
        digits = digits[2:]

    # ----------------------------------
    # PLACEHOLDERS ÓBVIOS
    # ----------------------------------

    if not digits:
        return None

    # Ex.: 99999999999, 00000000000
    if len(set(digits)) == 1:
        return None

    # Ex.: 11999999999
    if len(digits) >= 8:

        suffix = digits[-8:]

        if len(set(suffix)) == 1:
            return None

    # ----------------------------------
    # TELEFONE COM DDD
    # ----------------------------------

    if len(digits) == 10:

        return (
            f"({digits[:2]}) "
            f"{digits[2:6]}-"
            f"{digits[6:]}"
        )

    # ----------------------------------
    # CELULAR COM DDD
    # ----------------------------------

    if len(digits) == 11:

        return (
            f"({digits[:2]}) "
            f"{digits[2:7]}-"
            f"{digits[7:]}"
        )

    # ----------------------------------
    # TELEFONE LOCAL SEM DDD
    # ----------------------------------

    if len(digits) == 8:

        return (
            f"{digits[:4]}-"
            f"{digits[4:]}"
        )

    # Número inválido ou incompleto
    return None


def extract_contacts(html: str):

    html = html or ""

    email = None
    phone = None
    whatsapp = False

    # ----------------------------------
    # EMAIL
    # ----------------------------------

    emails = re.findall(
        EMAIL_PATTERN,
        html,
        re.IGNORECASE
    )

    print("\n==============================")
    print("EMAILS ENCONTRADOS")
    print("==============================")
    print(emails)

    for candidate in emails:

        print(
            "\nTestando:",
            candidate
        )

        if validate_email(candidate):

            email = candidate

            print("EMAIL ACEITO")

            break

        else:

            print("EMAIL REJEITADO")

    # ----------------------------------
    # TELEFONE
    # ----------------------------------

    phone_match = re.search(
        PHONE_PATTERN,
        html
    )

    if phone_match:

        raw_phone = phone_match.group(0)

        phone = normalize_phone(
            raw_phone
        )

        print("\n==============================")
        print("TELEFONE")
        print("==============================")
        print("RAW         :", raw_phone)
        print("NORMALIZADO :", phone)

    else:

        print("\n==============================")
        print("TELEFONE")
        print("==============================")
        print("NENHUM TELEFONE ENCONTRADO")

    # ----------------------------------
    # WHATSAPP
    # ----------------------------------

    for pattern in WHATSAPP_PATTERNS:

        if re.search(
            pattern,
            html,
            re.IGNORECASE
        ):

            whatsapp = True
            break

    # ----------------------------------
    # RESULTADO
    # ----------------------------------

    result = {

        "email": email,

        "email_score": calculate_email_score(
            email
        ),

        "telefone": phone,

        "tem_whatsapp": whatsapp

    }

    print("\nCONTACT EXTRACTOR")
    print(result)

    return result