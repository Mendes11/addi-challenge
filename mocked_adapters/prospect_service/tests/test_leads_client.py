import pytest

from domain_models.lead import Lead
from mocked_adapters.prospect_service.leads import MockedLeadsClient

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
        birth_date="1991-01-01",
        email="example2@example.com",
        converted=True
    )


@pytest.fixture
def client(lead1, lead2):
    return MockedLeadsClient({'test_id': lead1, 'test_id2': lead2})


async def test_get_not_converted_leads(lead1, client):
    assert await client.get_not_converted_leads() == [lead1]


async def get_lead(lead2, client):
    assert await client.get_lead("test_id2") == lead2


async def test_set_lead_converted(lead1, client):
    await client.set_lead_converted("test_id")
    assert lead1.converted


async def test_list_leads(client, lead1, lead2):
    assert await client.list_leads() == [lead1, lead2]
