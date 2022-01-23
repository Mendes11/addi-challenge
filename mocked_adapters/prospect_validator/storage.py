from typing import List

from domain_models.prospect import LeadValidationRequest
from domain_models.prospect_validator import Validation
from services.prospect_validator.ports.storage import ValidationsStorage


class InMemoryStorage(ValidationsStorage):
    def __init__(self):
        self.storage = {}

    async def store_validation(
        self, request: LeadValidationRequest, validation: Validation
    ):
        self.storage.setdefault(request.id, []).append(validation)

    async def get_request_validations(
        self, request: LeadValidationRequest
    ) -> List[Validation]:
        return self.storage.get(request.id, [])
