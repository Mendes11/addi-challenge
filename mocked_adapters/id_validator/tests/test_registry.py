import pytest

from mocked_adapters.id_validator.national_registry import \
    MockedNationalRegistryClient
from services.id_validator.ports.national_registry import RegistryInformation

pytestmark = pytest.mark.asyncio


@pytest.fixture
def registry():
    return {
        "test_id": RegistryInformation(
            national_id="test_id",
            birth_date="1992-01-01",
            first_name="John",
            last_name="Doe",
            email="example@example.com"
        ),
    }


async def test_check_registry_id_found(registry):
    cli = MockedNationalRegistryClient(registry)
    res = await cli.check_registry("test_id")
    assert res == registry["test_id"]


async def test_check_registry_not_found(registry):
    cli = MockedNationalRegistryClient(registry)
    res = await cli.check_registry("another_id")
    assert res is None
