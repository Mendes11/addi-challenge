from typing import List

from services.judicial_records_validator.ports.national_archives import \
    NationalArchivesClient


class MockedNationalArchivesClient(NationalArchivesClient):
    def __init__(self, archives: List[str]):
        self.archives = archives

    async def has_judicial_records(self, national_id: str) -> bool:
        return national_id in self.archives
