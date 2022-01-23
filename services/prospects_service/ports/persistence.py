from abc import ABC, abstractmethod
from typing import List

from domain_models.prospect import Prospect


class ProspectPersistence(ABC):
    @abstractmethod
    async def save_prospect(self, prospect: Prospect):
        ...

    @abstractmethod
    async def get_prospect(self, id_: str) -> Prospect:
        ...

    @abstractmethod
    async def list_prospects(self) -> List[Prospect]:
        ...


