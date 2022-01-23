from abc import ABC, abstractmethod


class LeadsServiceClient(ABC):
    """
    Interface to communicate with the Leads Service
    """

    @abstractmethod
    async def get_not_converted_leads(self):
        ...

    @abstractmethod
    async def get_lead(self, id_):
        ...

    @abstractmethod
    async def set_lead_converted(self, id_):
        ...

    @abstractmethod
    async def list_leads(self):
        ...
