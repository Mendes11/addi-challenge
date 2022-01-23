import asyncio

from domain_models.prospect_validator import LeadValidationResult
from services.prospect_validator.ports.sender import ValidationFinishedSender


class ProspectValidationFinishedSender(ValidationFinishedSender):
    def __init__(self):
        self.subscribers = set()

    def subscribe(self, callback):
        self.subscribers.add(callback)

    async def __call__(self, data: LeadValidationResult):
        coroutines = [
            callback(data) for callback in self.subscribers
        ]
        await asyncio.gather(*coroutines)
