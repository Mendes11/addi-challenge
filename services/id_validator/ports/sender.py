from abc import ABC, abstractmethod

from domain_models.id_validator import LeadValidated


class ValidationFinishedSender(ABC):
    """
    Notifies subscribers about the task completed
    """
    @abstractmethod
    async def __call__(self, data: LeadValidated):
        ...
