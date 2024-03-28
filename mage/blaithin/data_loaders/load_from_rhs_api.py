if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import requests
import json
from string import ascii_lowercase
import polars as pl 
from bs4 import BeautifulSoup

plant_type_mapping = {
    1: "Herbaceous Perennial",
    2: "Climber Wall Shrub",
    3: "Bedding",
    4: "Bulbs",
    5: "Ferns",
    6: "Shrubs",
    7: "Annual Biennial",
    8: "Alpine Rockery",
    9: "Roses",
    10: "Grasses",
    11: "Conservatory Greenhouse",
    12: "Fruit Edible",
    13: "Trees",
    14: "Houseplants",
    15: "Cactus Succulent",
    16: "Aquatic",
    17: "Bamboos",
    18: "Bogs",
    19: "Conifers",
    20: "Herbs",
    21: "Palms",
}

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Load data from the RHS API. This has very basic information contained within it.
    For now, we will just want to extract the botanical name and ID
    """

    plant_type = kwargs['plant_type']

    URL = "https://lwapp-uks-prod-psearch-01.azurewebsites.net/api/v1/plants/search/advanced"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    page_size = 1000

    plants = []


    for keywords in list(ascii_lowercase):
        temp_plants = []
        offset = 0

        while (
            response := requests.post(
                URL,
                json.dumps(
                    {
                        "includeAggregation": False,
                        "pageSize": page_size,
                        "startFrom": offset,
                        "plantTypes": [str(plant_type)],
                        "keywords": keywords,
                    }
                ),
                headers=headers,
            )
        ).status_code == 200:
            results = json.loads(response.text)["hits"]
            if len(results) == 0:
                # We have reached the end of this structure
                break
            for result in results:
                temp_plants.append(
                    {
                        "id": result["id"],
                        "botanical_name": BeautifulSoup(result["botanicalName"], "html.parser").text.strip(),
                    }
                )
            offset += page_size

        print(
            f"Found {len(temp_plants)} products for '{plant_type_mapping[plant_type]}' plant type and letter '{keywords}'"
        )
        plants.extend(temp_plants)        
    print(f"Total Found: {len(plants)} for '{plant_type_mapping[plant_type]}'")
    return pl.DataFrame(plants)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
