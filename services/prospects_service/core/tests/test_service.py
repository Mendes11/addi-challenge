from datetime import datetime

from mock import AsyncMock, call

import pytest

from domain_models.prospect_validator import LeadValidationResult
from services.prospects_service.core.service import ProspectService
from domain_models.lead import Lead
from domain_models.prospect import Prospect, LeadValidationRequest

pytestmark = pytest.mark.asyncio


@pytest.fixture
def leads_client():
    return AsyncMock()


@pytest.fixture
def validator():
    return AsyncMock()


@pytest.fixture
def storage():
    return AsyncMock()


async def test_service_convert_leads_client_called(leads_client, validator,
                                                   storage):
    svc = ProspectService(leads_client, validator, storage)
    await svc.convert_leads()
    leads_client.get_not_converted_leads.assert_awaited_once()


async def test_service_convert_leads_validator_called(
    leads_client, validator, storage
):
    lead1 = Lead(
        national_id='test_id',
        birth_date="1991-01-01",
        first_name="John",
        last_name="Doe",
        email="example@example.com"
    )
    lead2 = Lead(
        national_id='test2_id',
        birth_date="1992-01-01",
        first_name="John2",
        last_name="Doe2",
        email="example2@example.com"
    )
    leads_client.get_not_converted_leads.return_value = [lead1, lead2]
    svc = ProspectService(leads_client, validator, storage)
    await svc.convert_leads()

    validator.trigger_validation_request.assert_has_awaits(
        [call(lead1), call(lead2)],
        any_order=True
    )


async def test_conversion_valid_prospect_stored(
    leads_client, validator, storage
):
    lead = Lead(
        national_id='test_id',
        birth_date="1991-01-01",
        first_name="John",
        last_name="Doe",
        email="example@example.com"
    )
    result = LeadValidationResult(
        request=LeadValidationRequest(
            id=1, lead=lead, timestamp=datetime.utcnow()
        ),
        validations=[],
        score=70,
        is_valid=True
    )
    svc = ProspectService(leads_client, validator, storage)
    await svc.prospect_validation_finished(result)
    storage.save_prospect.assert_awaited_with(Prospect(**lead.dict()))


async def test_conversion_valid_lead_set_to_converted(
    leads_client, validator, storage
):
    lead = Lead(
        national_id='test_id',
        birth_date="1991-01-01",
        first_name="John",
        last_name="Doe",
        email="example@example.com"
    )
    req = LeadValidationRequest(id=1, lead=lead, timestamp=datetime.utcnow())
    result = LeadValidationResult(
        request=req,
        validations=[],
        score=61,
        is_valid=True
    )
    svc = ProspectService(leads_client, validator, storage)
    await svc.prospect_validation_finished(result)
    leads_client.set_lead_converted.assert_awaited_with("test_id")

async def test_conversion_not_valid_prospect_not_stored(
    leads_client, validator, storage
):
    lead = Lead(
        national_id='test_id',
        birth_date="1991-01-01",
        first_name="John",
        last_name="Doe",
        email="example@example.com"
    )
    req = LeadValidationRequest(id=1,lead=lead, timestamp=datetime.utcnow())
    result = LeadValidationResult(
        request=req,
        validations=[],
        score=60,
        is_valid=False
    )
    svc = ProspectService(leads_client, validator, storage)
    await svc.prospect_validation_finished(result)

    storage.save_prospect.assert_not_awaited()
    leads_client.set_lead_converted.assert_not_awaited()