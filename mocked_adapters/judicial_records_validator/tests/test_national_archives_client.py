import pytest

from mocked_adapters.judicial_records_validator.national_archives import \
    MockedNationalArchivesClient

pytestmark = pytest.mark.asyncio


async def test_has_judicial_records_found():
    cli = MockedNationalArchivesClient(["test_id1", "test_id2"])
    assert await cli.has_judicial_records("test_id1")


async def test_has_judicial_records_not_found():
    cli = MockedNationalArchivesClient(["test_id1", "test_id2"])
    assert not await cli.has_judicial_records("test_id3")
