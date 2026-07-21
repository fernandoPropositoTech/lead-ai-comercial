from app.services.qualification.qualification_engine import (
    calculate_qualification
)


def qualify_lead(lead):

    calculate_qualification(lead)

    return lead