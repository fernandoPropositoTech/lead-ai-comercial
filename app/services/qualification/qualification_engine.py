from app.services.qualification.qualification_rules import (
    qualifies
)


def calculate_qualification(lead):

    lead["qualificado"] = qualifies(lead)

    return lead