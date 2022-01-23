from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from pydantic import BaseModel


class RegistryInformation(BaseModel):
    national_id: str
    birth_date: date
    first_name: str
    last_name: str
    email: str


class NationalRegistryClient(ABC):
    @abstractmethod
    async def check_registry(self, id_: str) -> Optional[RegistryInformation]:
        """
        Call the National Registry Identification System and return the
        RegistryInformation of the specified id.

        In case it is not found, return None.

        :param id_: National ID
        :return: RegistryInformation or None if not found
        :rtype: RegistryInformation | None
        """
        ...
