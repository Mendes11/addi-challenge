from abc import ABC, abstractmethod

from domain_models.prospect_validator import LeadValidationResult


class ValidationFinishedSender(ABC):
    @abstractmethod
    async def __call__(self, data: LeadValidationResult):
        ...
