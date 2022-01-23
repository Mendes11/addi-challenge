from datetime import datetime

import pytest

from domain_models.lead import Lead
from domain_models.prospect import LeadValidationRequest
from domain_models.prospect_validator import Validation
from mocked_adapters.prospect_validator.qualification_service import \
    MockedQualificationService
from mocked_adapters.prospect_validator.storage import InMemoryStorage

pytestmark = pytest.mark.asyncio


@pytest.fixture
def storage():
    return InMemoryStorage()


@pytest.fixture
def validation_request(lead1):
    return LeadValidationRequest(
        id=1,
        lead=lead1,
        timestamp=datetime.utcnow()
    )


async def test_store_validation(storage, validation_request):
    validation = Validation(name="test", is_valid=False)
    await storage.store_validation(
        request=validation_request,
        validation=validation
    )

    assert storage.storage == {validation_request.id: [validation]}


async def test_store_validation_multiple(storage, validation_request):
    validation = Validation(name="test", is_valid=False)
    validation2 = Validation(name="test2", is_valid=True)
    storage.storage = {
        validation_request.id: [validation]
    }
    await storage.store_validation(
        request=validation_request,
        validation=validation2
    )

    assert storage.storage == {
        validation_request.id: [validation, validation2]
    }


async def test_get_request_validations(storage, validation_request):
    validation = Validation(name="test", is_valid=True)
    storage.storage = {
        validation_request.id: [validation]
    }

    assert await storage.get_request_validations(validation_request) == [
        validation]


async def test_validation_request_not_found(storage, validation_request):
    assert await storage.get_request_validations(validation_request) == []
