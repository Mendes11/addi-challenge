from datetime import date, datetime

from pydantic import BaseModel

from domain_models.lead import Lead


class Prospect(BaseModel):
    """
    A qualified Lead that was converted into a Prospect after the
    validation process.
    """
    national_id: str
    birth_date: date
    first_name: str
    last_name: str
    email: str


class LeadValidationRequest(BaseModel):
    id: int
    lead: Lead
    timestamp: datetime
