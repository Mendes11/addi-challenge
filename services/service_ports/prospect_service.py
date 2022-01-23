from abc import ABC, abstractmethod

from domain_models.prospect_validator import LeadValidationResult


class ProspectBaseService(ABC):
    """
    Core logic behind handling Prospects
    """
    # TODO Implement CRUD methods for external interaction

    @abstractmethod
    async def convert_leads(self):
        """
        Triggered by the user to start a Lead Validation SAGA for each
        available Lead from the Leads Service.
        """
        ...

    @abstractmethod
    async def prospect_validation_finished(self, result: LeadValidationResult):
        """
        Triggered whenever we receive a confirmation from our Lead
        Validation SAGA that it is a valid lead.
        """
        ...
