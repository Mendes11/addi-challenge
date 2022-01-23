import pytest

from domain_models.prospect import Prospect
from mocked_adapters.prospect_service.prospect_storage import ProspectStorage

pytestmark = pytest.mark.asyncio


@pytest.fixture
def prospect():
    return Prospect(
        national_id="test_id",
        first_name="John",
        last_name="Doe",
        birth_date="1990-01-01",
        email="example@example.com"
    )


async def test_save_prospect(prospect):
    storage = ProspectStorage()
    await storage.save_prospect(prospect)
    assert storage.prospects == {"test_id": prospect}


async def test_get_prospect(prospect):
    storage = ProspectStorage()
    storage.prospects = {"test_id": prospect}
    assert await storage.get_prospect("test_id") == prospect


async def test_list_prospects(prospect):
    storage = ProspectStorage()
    storage.prospects = {"test_id": prospect}

    assert await storage.list_prospects() == [prospect]
