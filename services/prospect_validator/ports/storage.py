from abc import ABC, abstractmethod
from typing import List

from domain_models.prospect import LeadValidationRequest
from domain_models.prospect_validator import Validation


class ValidationsStorage(ABC):
    @abstractmethod
    async def store_validation(
        self, request: LeadValidationRequest, validation: Validation
    ):
        ...

    @abstractmethod
    async def get_request_validations(self, request: LeadValidationRequest) \
        -> List[Validation]:
        ...
