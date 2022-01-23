from domain_models import id_validator, judicial_records_validator
from domain_models.prospect_validator import Validation, LeadValidationResult
from services.prospect_validator.ports.qualification_service import \
    ProspectQualificationServiceClient
from services.prospect_validator.ports.sender import ValidationFinishedSender
from services.prospect_validator.ports.storage import ValidationsStorage
from services.service_ports.prospect_validator import BaseProspectValidator


class ProspectValidator(BaseProspectValidator):
    def __init__(
        self,
        prospect_qualification_client: ProspectQualificationServiceClient,
        send_prospect_validation_finished: ValidationFinishedSender,
        storage: ValidationsStorage
    ):
        self.prospect_qualification_client = prospect_qualification_client
        self.send_prospect_validation_finished = send_prospect_validation_finished
        self.storage = storage

    async def check_all_validated(self, request):
        validations = await self.storage.get_request_validations(request)

        if len(validations) == 2:
            lead_score = await self.prospect_qualification_client.score_lead(
                request.lead, validations
            )
            is_valid = True if lead_score > 60 else False
            await self.send_prospect_validation_finished(
                LeadValidationResult(
                    request=request,
                    validations=validations,
                    score=lead_score,
                    is_valid=is_valid
                )
            )

    async def id_validator_finished(self, data: id_validator.LeadValidated):
        await self.storage.store_validation(
            data.validation_request,
            Validation(name="national_id_validation", is_valid=data.is_valid)
        )
        await self.check_all_validated(data.validation_request)

    async def judicial_records_validator_finished(
        self, data: judicial_records_validator.LeadValidated
    ):
        await self.storage.store_validation(
            data.validation_request,
            Validation(
                name="judicial_records_validation",
                is_valid=data.is_valid
            )
        )
        await self.check_all_validated(data.validation_request)
