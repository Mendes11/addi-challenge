from datetime import date

from pydantic import BaseModel


class Lead(BaseModel):
    """
    A Lead from the Leads Service
    """
    national_id: str
    birth_date: date
    first_name: str
    last_name: str
    email: str
    converted: bool = False


