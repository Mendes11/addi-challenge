from typing import List, Dict

from domain_models.lead import Lead
from domain_models.prospect_validator import Validation
from services.prospect_validator.ports.qualification_service import \
    ProspectQualificationServiceClient


class MockedQualificationService(ProspectQualificationServiceClient):
    def __init__(self, scores: Dict[str, int]):
        self.scores = scores

    async def score_lead(
        self,
        lead: Lead,
        validations: List[Validation]
    ) -> int:
        return self.scores.get(lead.national_id, 0)
