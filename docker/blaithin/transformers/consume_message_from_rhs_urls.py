from typing import Dict, List

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import polars as pl

@transformer
def transform(messages: List[Dict], *args, **kwargs):
    """
    Template code for a transformer block.

    Args:
        messages: List of messages in the stream.

    Returns:
        Transformed messages
    """
    session = HTMLSession()
    detailed_plants = []
    for msg in messages:
        id_ = msg['id']
        plant_url = msg['plant_url']
        botanical_name = msg['botanical_name']

        if (plant_page := session.get(plant_url)).status_code != 200:
            print(
                f"Given plant URL '{plant_url}' is incorrect. Plant botanical name: \"{botanical_name}\" and id {id}"
            )
            continue
        plant_content = BeautifulSoup(plant_page.content, "html.parser")

        try:
            common_name = plant_content.find("p", class_="summary summary--sub").text
            if common_name == "":
                print(f"Cannot find common name for plant {plant_url}")
                common_name = None
        except AttributeError:
            print(f"Cannot find common name for plant {plant_url}")
            common_name = None

        try:
            plant_type = [
                pt.text.strip()
                for pt in plant_content.find_all("span", class_="label ng-star-inserted")
            ]
        except AttributeError:
            print(f"Cannot find plant type for plant {plant_url}")
            plant_type = []

        try:
            description = plant_content.find("p", class_="ng-star-inserted").text.strip()
        except AttributeError:
            print(f"Cannot find description for plant {plant_url}")
            description = None

        try:
            plant_content.find("img", attrs={"alt": "RHS AGM"}).text
            is_rhs_award_winner = True
        except AttributeError:
            is_rhs_award_winner = False

        try:
            plant_content.find("img", attrs={"alt": "RHS Plants for pollinators"}).text
            is_pollinator_plant = True
        except AttributeError:
            is_pollinator_plant = False

        # Size, Growing Conditions, Colour&Scent, Position
        for plant_attributes_panel in plant_content.find_all(
            "div", class_="plant-attributes__panel"
        ):
            panel_heading = plant_attributes_panel.find(
                class_="plant-attributes__heading"
            ).text.lower()
            if panel_heading == "size":
                for attribute in plant_attributes_panel.find_all(class_="flag__body"):
                    if attribute.find(lambda tag: "Ultimate height" in tag.text):
                        height = (
                            attribute.contents[-1]
                            .strip()
                            .replace("–", "-")
                            .replace("â", "-")
                            .replace("-\x80\x93","-")
                        )
                    elif attribute.find(lambda tag: "Ultimate spread" in tag.text):
                        spread = (
                            attribute.contents[-1]
                            .strip()
                            .replace("–", "-")
                            .replace("â", "-")
                            .replace("-\x80\x93","-")
                        )
                    elif attribute.find(lambda tag: "Time to ultimate height" in tag.text):
                        time_to_ultimate_spread = (
                            attribute.contents[-1]
                            .strip()
                            .replace("–", "-")
                            .replace("â", "-")
                            .replace("-\x80\x93","-")
                        )
            elif panel_heading == "growing conditions":
                soils = [
                    soil_element.text
                    for soil_element in plant_attributes_panel.find_all(
                        "div", class_="flag__body"
                    )
                ]
                for attribute in plant_attributes_panel.find_all(class_="l-module"):
                    if attribute.find(lambda tag: "Moisture" in tag.text):
                        moisture = (
                            attribute.find("span")
                            .text.strip()
                            .replace("–", "-")
                            .replace("â", "-")
                            .replace("-\x80\x93","-")
                        )
                    elif attribute.find(lambda tag: "pH" in tag.text):
                        ph = [
                            attr.text.replace(",", "").strip()
                            for attr in attribute.find_all("span")
                        ]
            elif "colour" in panel_heading:
                if len(table := plant_attributes_panel.find("table")) > 0:
                    data = []
                    for row in table.find_all("tr")[1:]:
                        row_data = []
                        for header in row.find_all("th"):
                            row_data.append(header.text)
                        for cell in row.find_all("td"):
                            row_data.append(cell.text.strip().split())
                        data.append(row_data)
                    colour_and_scent = data
                    # df = pl.DataFrame(
                    #     data, schema=["Season", "Stem", "Flower", "Foliage", "Fruit"]
                    # )
                    # print(df)
            elif panel_heading == "position":
                sun_exposure = [
                    se.text
                    for se in plant_attributes_panel.find(
                        "ul", class_="list-inline ng-star-inserted"
                    ).find_all("li")
                ]

                aspect = [
                    asp.text.replace("\x80\x93", "-").replace("â", "").replace(" or ", "")
                    for asp in plant_attributes_panel.find("p").find_all("span")
                ]

                expos_hard = plant_attributes_panel.find(
                    "div", class_="l-row l-row--space l-row--auto-clear"
                ).find_all("div", class_="l-module")
                exposure = [
                    exp.text.replace(" or ", "") for exp in expos_hard[0].find_all("span")
                ]
                hardiness = expos_hard[1].find_all("span")[-1].text
        bottom_panel = plant_content.find("div", class_="panel__body").find_all(string=True)
        bottom_panel = [entry for entry in bottom_panel if entry.strip() != ""]
        i = 0
        while i < len(bottom_panel):
            value = bottom_panel[i]
            if str(value).strip().endswith(" or") or str(value).strip().endswith(","):
                bottom_panel[i] = bottom_panel[i] + bottom_panel[i + 1]
                del bottom_panel[i + 1]
                i -= 1
            i += 1

        bottom_panel_dict = {}
        for key, value in zip(bottom_panel[0::2], bottom_panel[1::2]):
            bottom_panel_dict[key] = value
        foliage = [entry.strip() for entry in bottom_panel_dict["Foliage"].split(" or ")]
        habit = [entry.strip() for entry in bottom_panel_dict["Habit"].split(",")]

        extract = {
            "id": id_,
            "source": "rhs",
            "plant_url": plant_url,
            "botanical_name": botanical_name,
            "common_name": common_name,
            "plant_type": plant_type,
            "description": description,
            "is_rhs_award_winner": is_rhs_award_winner,
            "is_pollinator_plant": is_pollinator_plant,
            "height": height,
            "spread": spread,
            "time_to_ultimate_spread": time_to_ultimate_spread,
            "soils": soils,
            "moisture": moisture,
            "ph": ph,
            #"colour_and_scent": colour_and_scent,
            "sun_exposure": sun_exposure,
            "aspect": aspect,
            "exposure": exposure,
            "hardiness": hardiness,
            "foliage": foliage,
            "habit": habit,
        }

        detailed_plants.append(extract)
    return detailed_plants