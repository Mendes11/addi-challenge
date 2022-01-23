from abc import ABC, abstractmethod

from domain_models import id_validator, judicial_records_validator


class BaseProspectValidator(ABC):
    """
    This service receives the parallel validations and, based on external
    checks with the prospect qualification system, determines if the lead
    is qualified to become a prospect or not
    """

    @abstractmethod
    async def id_validator_finished(self, data: id_validator.LeadValidated):
        ...

    @abstractmethod
    async def judicial_records_validator_finished(
        self, data: judicial_records_validator.LeadValidated
    ):
        ...
