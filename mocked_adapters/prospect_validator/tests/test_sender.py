from datetime import datetime

from mock import AsyncMock
import pytest

from domain_models.prospect import LeadValidationRequest
from domain_models.prospect_validator import LeadValidationResult
from mocked_adapters.prospect_validator.sender import \
    ProspectValidationFinishedSender

pytestmark = pytest.mark.asyncio


@pytest.fixture
def cli():
    return ProspectValidationFinishedSender()


async def test_callbacks_called(cli, lead1):
    callback1 = AsyncMock()
    callback2 = AsyncMock()
    cli.subscribe(callback1)
    cli.subscribe(callback2)

    data = LeadValidationResult(
        request=LeadValidationRequest(
            id=1,
            lead=lead1,
            timestamp=datetime.utcnow()
        ),
        validations=[],
        score=60,
        is_valid=False
    )

    await cli(data)

    callback1.assert_awaited_with(data)
    callback2.assert_awaited_with(data)
