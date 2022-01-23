from abc import ABC, abstractmethod

from domain_models.prospect import LeadValidationRequest


class BaseLeadValidator(ABC):
    @abstractmethod
    async def validation_requested(self, request: LeadValidationRequest):
        ...
