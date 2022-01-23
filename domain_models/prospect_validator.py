from typing import List

from pydantic import BaseModel

from domain_models.prospect import LeadValidationRequest


class Validation(BaseModel):
    name: str
    is_valid: bool


class LeadValidationResult(BaseModel):
    request: LeadValidationRequest  # Original request
    validations: List[Validation]  # All validations from the SAGA
    score: int
    is_valid: bool  # Final Decision
