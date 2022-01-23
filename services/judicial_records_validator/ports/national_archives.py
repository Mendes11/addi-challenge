from abc import ABC, abstractmethod


class NationalArchivesClient(ABC):
    @abstractmethod
    async def has_judicial_records(self, national_id: str) -> bool:
        ...
