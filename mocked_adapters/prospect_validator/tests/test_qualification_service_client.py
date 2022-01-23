import pytest

from domain_models.lead import Lead
from mocked_adapters.prospect_validator.qualification_service import \
    MockedQualificationService

pytestmark = pytest.mark.asyncio


@pytest.fixture
def lead():
    return Lead(
        national_id="test_id",
        first_name="John",
        last_name="Doe",
        birth_date="1990-01-01",
        email="example@example.com"
    )


async def test_service_client_score_lead(lead):
    lead.national_id = "test_id1"
    cli = MockedQualificationService({"test_id1": 50, "test_id2": 30})
    assert await cli.score_lead(lead, []) == 50


async def test_service_client_score_lead_not_found(lead):
    lead.national_id = "test_id3"
    cli = MockedQualificationService({"test_id1": 50, "test_id2": 30})
    assert await cli.score_lead(lead, []) == 0
