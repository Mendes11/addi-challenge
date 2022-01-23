import asyncio

from domain_models.lead import Lead
from services.id_validator.ports.national_registry import RegistryInformation

from setup import new_judicial_validator, new_prospect_validator, \
    new_national_validator, new_prospects_service

leads = {
    "id1": Lead(
        national_id="id1",
        birth_date="1992-01-01",
        first_name="Josh",
        last_name="Smith",
        email="josh.smith@example.com",
    ),
    "id2": Lead(
        national_id="id2",
        birth_date="1991-01-01",
        first_name="Alex",
        last_name="Something",
        email="alex.something@example.com",
    ),
    "id3": Lead(
        national_id="id3",
        birth_date="1990-01-01",
        first_name="Josh",
        last_name="Doe",
        email="josh.doe@example.com",
        converted=True # This Guy won't be used due to this.
    ),
}

registry_infos = {
    "id1": RegistryInformation(
        national_id="id1",
        birth_date="1989-01-01",  # Not Match with Lead information
        first_name="Josh",
        last_name="Smith",
        email="josh.smith@example.com",
    ),
    "id2": RegistryInformation(
        national_id="id2",
        birth_date="1991-01-01",
        first_name="Alex",
        last_name="Something",
        email="alex.something@example.com",
    ),
    "id3": RegistryInformation(
        national_id="id3",
        birth_date="1990-01-01",
        first_name="Josh",
        last_name="Doe",
        email="josh.doe@example.com",
        converted=True
    ),
}
judicial_records = ["id2"]

scores = {
    "id1": 55,
    "id2": 80,
}

prospect_validator = new_prospect_validator(scores)

id_validator = new_national_validator(prospect_validator, registry_infos)
judicial_validator = new_judicial_validator(prospect_validator, ["id2"])

prospects_service = new_prospects_service(
    id_validator, judicial_validator, leads
)

# Finally, we generate the subscriptions for the prospect_validator events
prospect_validator.send_prospect_validation_finished.subscribe(
    prospects_service.prospect_validation_finished
)


async def run_main():
    await prospects_service.convert_leads()

    # Now Prints the Leads and the Prospects
    print("Result\n")
    print("Leads:")
    print(
        '\n'.join(
            [f"{lead.national_id} - converted = {lead.converted}"
             for lead in await prospects_service.leads_client.list_leads()]
        )
    )
    print("\nProspects:")
    print(
        '\n'.join(
            [f"{prospect.national_id}" for prospect in
             await prospects_service.storage.list_prospects()]
        )
    )


if __name__ == "__main__":
    """
    Expectations:

    * Lead1:
        * National ID Validation = False
        * Judicial Records Validation = True
        * Score = 55
        * Convert to Prospect? = NO

    * Lead2:
        * National ID Validation = True
        * Judicial Records Validation = False
        * Score = 80
        * Convert to Prospect? = YES

    * Lead3:
        Already Converted, so it won't be used

    """

    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_main())
