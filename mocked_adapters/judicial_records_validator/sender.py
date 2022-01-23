import asyncio

from domain_models.id_validator import LeadValidated
from services.judicial_records_validator.ports.sender import ValidationFinishedSender


class JudicialValidatorFinishedSender(ValidationFinishedSender):
    def __init__(self):
        self.subscribers = set()

    def subscribe(self, callback):
        self.subscribers.add(callback)

    async def __call__(self, data: LeadValidated):
        coroutines = [
            callback(data) for callback in self.subscribers
        ]
        await asyncio.gather(*coroutines)
