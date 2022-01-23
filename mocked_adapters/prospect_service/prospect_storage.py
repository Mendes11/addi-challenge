from typing import List

from domain_models.prospect import Prospect
from services.prospects_service.ports.persistence import ProspectPersistence


class ProspectStorage(ProspectPersistence):
    def __init__(self):
        self.prospects = {}

    async def save_prospect(self, prospect: Prospect):
        self.prospects[prospect.national_id] = prospect

    async def get_prospect(self, id_: str) -> Prospect:
        return self.prospects.get(id_)

    async def list_prospects(self) -> List[Prospect]:
        return list(self.prospects.values())
