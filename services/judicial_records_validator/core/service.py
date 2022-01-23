from domain_models.judicial_records_validator import LeadValidated
from domain_models.prospect import LeadValidationRequest
from services.judicial_records_validator.ports.national_archives import \
    NationalArchivesClient
from services.judicial_records_validator.ports.sender import ValidationFinishedSender
from services.service_ports.validator import BaseLeadValidator


class JudicialRecordsValidator(BaseLeadValidator):
    def __init__(
        self,
        national_archives_client: NationalArchivesClient,
        send_validation_finished: ValidationFinishedSender
    ):
        self.national_archives_client = national_archives_client
        self.send_validation_finished = send_validation_finished

    async def validation_requested(self, request: LeadValidationRequest):
        has_judicial_records = await self.national_archives_client.has_judicial_records(
            request.lead.national_id
        )
        await self.send_validation_finished(
            LeadValidated(
                validation_request=request, is_valid=not has_judicial_records
            )
        )
