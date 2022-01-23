import pytest

from domain_models.lead import Lead


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
