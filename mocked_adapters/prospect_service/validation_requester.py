import asyncio
from datetime import datetime

from domain_models.lead import Lead
from domain_models.prospect import LeadValidationRequest
from services.prospects_service.ports.validation_requester import ValidationRequester


class InMemoryValidationRequester(ValidationRequester):
    """
    Instead of using a broker for events triggering, we will implement a
    subscription system where all services drivers will be passed as the
    subscribers
    """

    def __init__(self):
        self.subscribers = set()
        self.last_id = 0

    def subscribe(self, callback):
        self.subscribers.add(callback)

    async def trigger_validation_request(self, lead: Lead):
        req = LeadValidationRequest(
            id=self.last_id + 1, lead=lead, timestamp=datetime.utcnow()
        )
        coroutines = [
            callback(req) for callback in self.subscribers
        ]
        self.last_id += 1
        await asyncio.gather(*coroutines)
