from pydantic import BaseModel

from domain_models.prospect import LeadValidationRequest


class LeadValidated(BaseModel):
    validation_request: LeadValidationRequest
    is_valid: bool
