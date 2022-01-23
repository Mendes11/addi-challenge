from domain_models.id_validator import LeadValidated
from domain_models.lead import Lead
from domain_models.prospect import LeadValidationRequest
from services.id_validator.ports.national_registry import NationalRegistryClient, \
    RegistryInformation
from services.id_validator.ports.sender import ValidationFinishedSender
from services.service_ports.validator import BaseLeadValidator


class NationalIDValidator(BaseLeadValidator):
    def __init__(
        self,
        national_registry_client: NationalRegistryClient,
        send_validation_finished: ValidationFinishedSender
    ):
        self.national_registry_client = national_registry_client
        self.send_validation_finished = send_validation_finished

    def lead_info_match(self, lead: Lead, registry_info: RegistryInformation):
        # Using the fact that I used the same field names/types for both
        return lead == Lead(**registry_info.dict())

    async def validation_requested(self, request: LeadValidationRequest):
        registry_info = await self.national_registry_client.check_registry(
            request.lead.national_id
        )
        is_valid = False
        if registry_info:
            is_valid = self.lead_info_match(request.lead, registry_info)
        result = LeadValidated(validation_request=request, is_valid=is_valid)
        await self.send_validation_finished(result)
