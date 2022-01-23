import pytest
from mock import AsyncMock

from domain_models.id_validator import LeadValidated
from domain_models.lead import Lead
from domain_models.prospect import LeadValidationRequest
from services.id_validator.core.service import NationalIDValidator
from services.id_validator.ports.national_registry import RegistryInformation

pytestmark = pytest.mark.asyncio


@pytest.fixture
def national_registry_client():
    return AsyncMock()


@pytest.fixture
def send_validation_finished():
    return AsyncMock()


@pytest.fixture
def lead():
    return Lead(
        national_id="test_id", birth_date="2021-01-01", first_name="John",
        last_name="Doe", email="email@example.com"
    )


@pytest.fixture
def registry_info():
    return RegistryInformation(
        national_id="test_id", birth_date="2021-01-01", first_name="John",
        last_name="Doe", email="email@example.com"
    )


async def test_lead_information_matching(
    national_registry_client, send_validation_finished, lead, registry_info
):
    svc = NationalIDValidator(
        national_registry_client, send_validation_finished
    )
    assert svc.lead_info_match(lead, registry_info)


async def test_lead_information_not_match(
    national_registry_client, send_validation_finished, lead, registry_info
):
    registry_info.last_name = "Cena"

    svc = NationalIDValidator(
        national_registry_client, send_validation_finished
    )
    assert not svc.lead_info_match(lead, registry_info)


async def test_validation_requested_registry_checked(
    national_registry_client, send_validation_finished, lead, registry_info
):
    national_registry_client.check_registry.return_value = registry_info
    svc = NationalIDValidator(
        national_registry_client, send_validation_finished
    )
    req = LeadValidationRequest(
        id=1, lead=lead, timestamp="2022-01-01T00:00:00Z"
    )
    await svc.validation_requested(req)

    national_registry_client.check_registry.assert_awaited_with(
        lead.national_id
    )


async def test_validation_requested_finished_event_sent(
    national_registry_client, send_validation_finished, lead, registry_info
):
    national_registry_client.check_registry.return_value = registry_info
    svc = NationalIDValidator(
        national_registry_client, send_validation_finished
    )
    req = LeadValidationRequest(
        id=1, lead=lead, timestamp="2022-01-01T00:00:00Z"
    )
    await svc.validation_requested(req)

    send_validation_finished.assert_awaited_with(
        LeadValidated(validation_request=req, is_valid=True)
    )


async def test_validation_requested_registry_checked_not_found(
    national_registry_client, send_validation_finished, lead
):
    national_registry_client.check_registry.return_value = None
    svc = NationalIDValidator(
        national_registry_client, send_validation_finished
    )
    req = LeadValidationRequest(
        id=1, lead=lead, timestamp="2022-01-01T00:00:00Z"
    )
    await svc.validation_requested(req)
    send_validation_finished.assert_awaited_with(
        LeadValidated(validation_request=req, is_valid=False)
    )
