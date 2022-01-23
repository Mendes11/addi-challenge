from services.prospects_service.ports.leads import LeadsServiceClient


class MockedLeadsClient(LeadsServiceClient):
    def __init__(self, leads):
        self.leads = leads

    async def get_not_converted_leads(self):
        return list(filter(lambda x: not x.converted, self.leads.values()))

    async def get_lead(self, id_):
        return self.leads.get(id_)

    async def set_lead_converted(self, id_):
        lead = self.leads.get(id_)
        if lead:
            lead.converted = True

    async def list_leads(self):
        return list(self.leads.values())