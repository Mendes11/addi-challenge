from mock import AsyncMock
import pytest

from domain_models import id_validator, judicial_records_validator
from domain_models.lead import Lead
from domain_models.prospect import LeadValidationRequest
from domain_models.prospect_validator import Validation, LeadValidationResult
from services.prospect_validator.core.service import ProspectValidator

pytestmark = pytest.mark.asyncio


@pytest.fixture
def storage():
    return AsyncMock()


@pytest.fixture
def prospect_client():
    return AsyncMock()


@pytest.fixture
def send_finished():
    return AsyncMock()


@pytest.fixture
def lead():
    return Lead(
        national_id="test_id", birth_date="2021-01-01", first_name="John",
        last_name="Doe", email="email@example.com"
    )


@pytest.fixture
def validation_request(lead):
    return LeadValidationRequest(
        id=1, lead=lead, timestamp="2022-01-01T00:00:00Z"
    )


async def test_check_all_validated_length_1_nothing_called(
    prospect_client, send_finished, storage, validation_request
):
    storage.get_request_validations.return_value = [
        Validation(name="Test", is_valid=False)
    ]
    svc = ProspectValidator(prospect_client, send_finished, storage)
    await svc.check_all_validated(validation_request)

    prospect_client.score_lead.assert_not_awaited()
    send_finished.assert_not_awaited()


async def test_check_all_validated_length_2_score_valid(
    prospect_client, send_finished, storage, validation_request, lead
):
    validations = [
        Validation(name="Test", is_valid=False),
        Validation(name="Test2", is_valid=False),
    ]
    storage.get_request_validations.return_value = validations
    prospect_client.score_lead.return_value = 61

    svc = ProspectValidator(prospect_client, send_finished, storage)
    await svc.check_all_validated(validation_request)

    prospect_client.score_lead.assert_awaited_with(
        lead, validations
    )
    send_finished.assert_awaited_with(
        LeadValidationResult(
            request=validation_request, validations=validations,
            score=61, is_valid=True
        )
    )


async def test_check_all_validated_length_2_score_invalid(
    prospect_client, send_finished, storage, validation_request, lead
):
    validations = [
        Validation(name="Test", is_valid=False),
        Validation(name="Test2", is_valid=False),
    ]
    storage.get_request_validations.return_value = validations
    prospect_client.score_lead.return_value = 60

    svc = ProspectValidator(prospect_client, send_finished, storage)
    await svc.check_all_validated(validation_request)

    prospect_client.score_lead.assert_awaited_with(
        lead, validations
    )
    send_finished.assert_awaited_with(
        LeadValidationResult(
            request=validation_request, validations=validations,
            score=60, is_valid=False
        )
    )


async def test_judicial_records_finished_validation_stored(
    prospect_client, send_finished, storage, validation_request, mocker
):
    event_data = judicial_records_validator.LeadValidated(
        validation_request=validation_request,
        is_valid=True
    )

    svc = ProspectValidator(prospect_client, send_finished, storage)
    check_all_validated = mocker.patch.object(
        svc, "check_all_validated", new=AsyncMock()
    )
    await svc.judicial_records_validator_finished(event_data)

    storage.store_validation.assert_awaited_with(
        validation_request,
        Validation(name="judicial_records_validation", is_valid=True)
    )
    check_all_validated.assert_awaited_with(validation_request)


async def test_judicial_records_finished_validation_stored_invalid(
    prospect_client, send_finished, storage, validation_request, mocker
):
    event_data = judicial_records_validator.LeadValidated(
        validation_request=validation_request,
        is_valid=False
    )

    svc = ProspectValidator(prospect_client, send_finished, storage)
    check_all_validated = mocker.patch.object(
        svc, "check_all_validated", new=AsyncMock()
    )
    await svc.judicial_records_validator_finished(event_data)

    storage.store_validation.assert_awaited_with(
        validation_request,
        Validation(name="judicial_records_validation", is_valid=False)
    )
    check_all_validated.assert_awaited_with(validation_request)


async def test_id_validator_finished_validation_stored(
    prospect_client, send_finished, storage, validation_request,
    mocker
):
    event_data = id_validator.LeadValidated(
        validation_request=validation_request,
        is_valid=True
    )
    svc = ProspectValidator(prospect_client, send_finished, storage)
    check_all_validated = mocker.patch.object(
        svc, "check_all_validated", new=AsyncMock()
    )

    await svc.id_validator_finished(event_data)

    storage.store_validation.assert_awaited_with(
        validation_request,
        Validation(name="national_id_validation", is_valid=True)
    )
    check_all_validated.assert_awaited_with(
        validation_request
    )


async def test_id_validator_finished_validation_invalid(
    prospect_client, send_finished, storage, validation_request,
    mocker
):
    event_data = id_validator.LeadValidated(
        validation_request=validation_request,
        is_valid=False
    )

    svc = ProspectValidator(prospect_client, send_finished, storage)
    check_all_validated = mocker.patch.object(
        svc, "check_all_validated", new=AsyncMock()
    )
    await svc.id_validator_finished(event_data)

    storage.store_validation.assert_awaited_with(
        validation_request,
        Validation(name="national_id_validation", is_valid=False)
    )
    check_all_validated.assert_awaited_with(
        validation_request
    )
