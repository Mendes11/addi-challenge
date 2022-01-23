import asyncio

from domain_models.prospect import Prospect
from domain_models.prospect_validator import LeadValidationResult
from services.prospects_service.ports.leads import LeadsServiceClient
from services.prospects_service.ports.persistence import ProspectPersistence
from services.service_ports.prospect_service import ProspectBaseService
from services.prospects_service.ports.validation_requester import \
    ValidationRequester


class ProspectService(ProspectBaseService):
    def __init__(
        self,
        leads_client: LeadsServiceClient,
        validator: ValidationRequester,
        storage: ProspectPersistence
    ):
        self.leads_client = leads_client
        self.validator = validator
        self.storage = storage

    async def convert_leads(self):
        leads = await self.leads_client.get_not_converted_leads()
        tasks = [self.validator.trigger_validation_request(lead) for lead in
                 leads]
        await asyncio.gather(*tasks)

    async def prospect_validation_finished(self, result: LeadValidationResult):
        lead = result.request.lead
        print(f"Received a Finished result for lead: {lead.national_id}")
        print(f"Lead {lead.national_id} validation is {result.is_valid}")
        if result.is_valid:
            prospect = Prospect(**lead.dict())
            await self.storage.save_prospect(prospect)
            await self.leads_client.set_lead_converted(lead.national_id)
