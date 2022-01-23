from typing import Optional, Dict

from services.id_validator.ports.national_registry import \
    NationalRegistryClient, RegistryInformation


class MockedNationalRegistryClient(NationalRegistryClient):
    def __init__(self, registry: Dict[str, RegistryInformation]):
        self.registry = registry

    async def check_registry(self, id_: str) -> Optional[RegistryInformation]:
        return self.registry.get(id_)
