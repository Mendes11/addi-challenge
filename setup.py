from typing import List, Dict

from domain_models.lead import Lead
from mocked_adapters.id_validator.national_registry import \
    MockedNationalRegistryClient
from mocked_adapters.id_validator.sender import IDValidationFinishedSender
from mocked_adapters.judicial_records_validator.national_archives import \
    MockedNationalArchivesClient
from mocked_adapters.judicial_records_validator.sender import \
    JudicialValidatorFinishedSender
from mocked_adapters.prospect_service.leads import MockedLeadsClient
from mocked_adapters.prospect_service.prospect_storage import ProspectStorage
from mocked_adapters.prospect_service.validation_requester import \
    InMemoryValidationRequester
from mocked_adapters.prospect_validator.qualification_service import \
    MockedQualificationService
from mocked_adapters.prospect_validator.sender import \
    ProspectValidationFinishedSender
from mocked_adapters.prospect_validator.storage import InMemoryStorage
from services.id_validator.core.service import NationalIDValidator
from services.id_validator.ports.national_registry import RegistryInformation
from services.judicial_records_validator.core.service import \
    JudicialRecordsValidator
from services.prospect_validator.core.service import ProspectValidator
from services.prospects_service.core.service import ProspectService
from services.service_ports.prospect_service import ProspectBaseService
from services.service_ports.prospect_validator import BaseProspectValidator
from services.service_ports.validator import BaseLeadValidator


def new_judicial_validator(
    prospect_validator: BaseProspectValidator,
    ids_with_judicial_records: List[str]
) -> BaseLeadValidator:
    national_archives_client = MockedNationalArchivesClient(
        ids_with_judicial_records)
    send_judicial_validation_finished = JudicialValidatorFinishedSender()
    send_judicial_validation_finished.subscribe(
        prospect_validator.judicial_records_validator_finished
    )
    judicial_validator = JudicialRecordsValidator(
        national_archives_client, send_judicial_validation_finished
    )
    return judicial_validator


def new_prospect_validator(
    leads_scores: Dict[str, int]) -> BaseProspectValidator:
    qualification_client = MockedQualificationService(leads_scores)
    validation_finished_sender = ProspectValidationFinishedSender()
    prospect_validator_storage = InMemoryStorage()
    prospect_validator = ProspectValidator(
        qualification_client, validation_finished_sender,
        prospect_validator_storage
    )
    return prospect_validator


def new_national_validator(
    prospect_validator: BaseProspectValidator,
    registries: RegistryInformation
) -> BaseLeadValidator:
    national_registry_client = MockedNationalRegistryClient(registries)
    send_id_validation_finished = IDValidationFinishedSender()
    send_id_validation_finished.subscribe(
        prospect_validator.id_validator_finished
    )
    id_validator = NationalIDValidator(
        national_registry_client, send_id_validation_finished
    )
    return id_validator


def new_prospects_service(
    id_validator: BaseLeadValidator, judicial_validator: BaseLeadValidator,
    leads: List[Lead]
) -> ProspectBaseService:
    mocked_leads = MockedLeadsClient(leads)
    validation_requested = InMemoryValidationRequester()
    validation_requested.subscribe(
        id_validator.validation_requested,
    )
    validation_requested.subscribe(
        judicial_validator.validation_requested,
    )
    prospects_storage = ProspectStorage()
    prospects_service = ProspectService(
        mocked_leads, validation_requested, prospects_storage
    )
    return prospects_service
