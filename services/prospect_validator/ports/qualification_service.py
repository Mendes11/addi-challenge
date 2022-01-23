from abc import ABC, abstractmethod
from typing import List

from domain_models.lead import Lead
from domain_models.prospect_validator import Validation


class ProspectQualificationServiceClient(ABC):
    """
    Client to communicate with external Prospect Qualifications Service in
    order to verify if the lead is a valid prospect.
    """

    @abstractmethod
    async def score_lead(
        self,
        lead: Lead,
        validations: List[Validation]
    ) -> int:
        ...
