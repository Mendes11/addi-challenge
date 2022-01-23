from datetime import datetime

import pytest
from mock import AsyncMock, call

from domain_models.lead import Lead
from domain_models.prospect import LeadValidationRequest
from mocked_adapters.prospect_service.validation_requester import \
    InMemoryValidationRequester

pytestmark = pytest.mark.asyncio


@pytest.fixture
def lead1():
    return Lead(
        national_id="test_id",
        first_name="John",
        last_name="Doe",
        birth_date="1990-01-01",
        email="example@example.com"
    )


@pytest.fixture
def lead2():
    return Lead(
        national_id="test_id2",
        first_name="John2",
        last_name="Doe2",
        birth_date="1990-01-01",
        email="example@example.com"
    )


@pytest.fixture
def callback1():
    return AsyncMock()


@pytest.fixture
def callback2():
    return AsyncMock()


@pytest.fixture
def requester(callback1, callback2):
    requester = InMemoryValidationRequester()
    requester.subscribe(callback1)
    requester.subscribe(callback2)
    return requester


async def test_trigger_validation_request_subscribers_called(
    requester, mocker, callback1, callback2, lead1
):
    datetime_mock = mocker.patch(
        "mocked_adapters.prospect_service.validation_requester.datetime"
    )

    datetime_mock.utcnow.return_value = datetime(2022, 1, 1)
    await requester.trigger_validation_request(lead1)

    callback1.assert_awaited_with(
        LeadValidationRequest(
            id=1, lead=lead1, timestamp=datetime(2022, 1, 1)
        )
    )
    callback2.assert_awaited_with(
        LeadValidationRequest(
            id=1, lead=lead1, timestamp=datetime(2022, 1, 1)
        )
    )


async def test_trigger_validation_request_request_id_incremented(
    requester, mocker, callback1, callback2, lead1, lead2
):
    datetime_mock = mocker.patch(
        "mocked_adapters.prospect_service.validation_requester.datetime"
    )

    datetime_mock.utcnow.return_value = datetime(2022, 1, 1)
    await requester.trigger_validation_request(lead1)

    # Call Again
    datetime_mock.utcnow.return_value = datetime(2022, 1, 1)
    await requester.trigger_validation_request(lead2)

    callback1.assert_has_awaits(
        [
            call(
                LeadValidationRequest(
                    id=1, lead=lead1, timestamp=datetime(2022, 1, 1)
                )
            ),
            call(
                LeadValidationRequest(
                    id=2, lead=lead2, timestamp=datetime(2022, 1, 1)
                )
            ),
        ]
    )

    callback2.assert_has_awaits(
        [
            call(
                LeadValidationRequest(
                    id=1, lead=lead1, timestamp=datetime(2022, 1, 1)
                )
            ),
            call(
                LeadValidationRequest(
                    id=2, lead=lead2, timestamp=datetime(2022, 1, 1)
                )
            ),
        ]
    )
