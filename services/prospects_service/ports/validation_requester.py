from abc import ABC, abstractmethod


class ValidationRequester(ABC):
    @abstractmethod
    async def trigger_validation_request(self, lead):
        """
        An asynchronous operation that we expect to dispatch an event that
        will in turn trigger a validation system.

        :param lead: Lead object to be sent in the event
        """
        ...
