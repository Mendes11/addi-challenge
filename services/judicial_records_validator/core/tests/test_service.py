import pytest
from mock import AsyncMock

from domain_models.judicial_records_validator import LeadValidated
from domain_models.lead import Lead
from domain_models.prospect import LeadValidationRequest
from services.judicial_records_validator.core.service import JudicialRecordsValidator

pytestmark = pytest.mark.asyncio


@pytest.fixture
def national_archives_client():
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


async def test_validation_requested_with_judicial_records(
    national_archives_client, send_validation_finished, lead
):
    national_archives_client.has_judicial_records.return_value = True
    req = LeadValidationRequest(
        id=1, lead=lead, timestamp="2022-01-01T00:00:00Z"
    )
    svc = JudicialRecordsValidator(
        national_archives_client, send_validation_finished
    )
    await svc.validation_requested(req)
    national_archives_client.has_judicial_records.assert_awaited_with(
        lead.national_id
    )
    send_validation_finished.assert_called_with(
        LeadValidated(
            validation_request=req, is_valid=False
        )
    )


async def test_validation_requested_without_judicial_records(
    national_archives_client, send_validation_finished, lead
):
    national_archives_client.has_judicial_records.return_value = False
    req = LeadValidationRequest(
        id=1, lead=lead, timestamp="2022-01-01T00:00:00Z"
    )
    svc = JudicialRecordsValidator(
        national_archives_client, send_validation_finished
    )
    await svc.validation_requested(req)

    send_validation_finished.assert_called_with(
        LeadValidated(
            validation_request=req, is_valid=True
        )
    )
