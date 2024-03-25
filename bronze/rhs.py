import requests
import json
from bs4 import BeautifulSoup
import re


def get_plant_urls(
    plantTypes: list = range(1, 22),
    habits: list = range(1, 13),
    spreads: list = range(1, 9),
):
    URL = "https://lwapp-uks-prod-psearch-01.azurewebsites.net/api/v1/plants/search/advanced"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    page_size = 1000
    plant_urls = []

    for plantType in plantTypes:
        for habit in habits:
            for spread in spreads:
                temp_plant_urls = []
                offset = 0

                while (
                    response := requests.post(
                        URL,
                        json.dumps(
                            {
                                "includeAggregation": False,
                                "pageSize": page_size,
                                "startFrom": offset,
                                "habits": [str(habit)],
                                "plantTypes": [str(plantType)],
                                "spread": [str(spread)],
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
                        botanical_name = result["botanicalName"]
                        id = result["id"]

                        # Prep botanical name
                        botanical_name_base = BeautifulSoup(
                            botanical_name, "html.parser"
                        )
                        botanical_name_base = (
                            botanical_name_base.text.strip()
                        )  # Get text between html characters
                        botanical_name_html = (
                            botanical_name_base.replace(" ", "-")
                            .replace("/", "-")
                            .replace("-&-", "-")
                        )  # replace special characters with -
                        botanical_name_html = botanical_name_html.replace(
                            ".", ""
                        )  # replace certain characters with .
                        botanical_name_html = re.sub(r"[']", "", botanical_name_html)

                        plant_url = f"https://www.rhs.org.uk/plants/{id}/{botanical_name_html}/details"
                        temp_plant_urls.append(
                            {
                                "id": id,
                                "botanical_name": botanical_name_base,
                                "plant_url": plant_url,
                                "source": "rhs_urls",
                            }
                        )
                    offset += page_size

                print(
                    f"Found {len(temp_plant_urls)} products for habit [{str(habit)}], plantType [{str(plantType)}], spread [{str(spread)}]"
                )
                plant_urls.extend(temp_plant_urls)

    return plant_urls
