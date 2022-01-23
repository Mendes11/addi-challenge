from datetime import datetime

import pytest
from mock import AsyncMock

from domain_models.judicial_records_validator import LeadValidated
from domain_models.lead import Lead
from domain_models.prospect import LeadValidationRequest
from mocked_adapters.judicial_records_validator.sender import \
    JudicialValidatorFinishedSender

pytestmark = pytest.mark.asyncio


@pytest.fixture
def lead():
    return Lead(
        national_id="test_id",
        birth_date="1992-01-01",
        first_name="John",
        last_name="Doe",
        email="example@example.com"
    )


async def test_sender_subscribers_called(lead):
    sender = JudicialValidatorFinishedSender()
    callback1 = AsyncMock()
    callback2 = AsyncMock()
    sender.subscribe(callback1)
    sender.subscribe(callback2)

    data = LeadValidated(
        validation_request=LeadValidationRequest(
            id=1, lead=lead, timestamp=datetime.utcnow()
        ),
        is_valid=True
    )
    await sender(data)

    callback1.assert_awaited_with(data)
    callback2.assert_awaited_with(data)
