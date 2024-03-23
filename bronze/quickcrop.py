#!/usr/bin/env python
# coding: utf-8
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import importlib


def selenium_setup() -> webdriver:
    driver = webdriver.Chrome()
    driver.get("https://www.quickcrop.ie")
    WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable(
            (
                By.XPATH,
                "//button[@class='sd-button-widget calashock-categories-widget__button button button--primary'][text()='ACCEPT ALL COOKIES']",
            )
        )
    ).click()

    ## Implicit waits weren't working. The modal seems to take time to close
    time.sleep(1)

    return driver


multibuy_pattern_deal = re.compile(r"(\d+ x \w+)")
multibuy_pattern_trees = re.compile(r"(\d+ Trees)", flags=re.IGNORECASE)
multibuy_pattern_multipack = re.compile(r"(\d+ Pack)", flags=re.IGNORECASE)

numeric_pattern_compiled = re.compile(r"(\d+)")


multibuy_pattern_deal = re.compile(r"(\d+ x \w+)")
multibuy_pattern_trees = re.compile(r"(\d+ Tree)", flags=re.IGNORECASE)
multibuy_pattern_pack = re.compile(r"(\d+ Pack)", flags=re.IGNORECASE)
multibuy_pattern_plant = re.compile(r"(\d+ Plant)", flags=re.IGNORECASE)

numeric_pattern_compiled = re.compile(r"(\d+)")


def extract_quantity_from_text(product_text: str) -> tuple[int, bool]:
    multibuy_str = (
        re.search(multibuy_pattern_deal, product_text)
        or re.search(multibuy_pattern_trees, product_text)
        or re.search(multibuy_pattern_pack, product_text)
        or re.search(multibuy_pattern_plant, product_text)
    )
    if multibuy_str:
        quantity = int(
            re.search(numeric_pattern_compiled, multibuy_str.group(0)).group(0)
        )
        multibuy = True
    else:
        quantity = 1
        multibuy = False
    return quantity, multibuy


size_pattern_litres = re.compile(r"(0?\.?\d+\s?L)")
size_pattern_centimetres = re.compile(r"(\d+\s?-\s?\d+\s?cm)", flags=re.IGNORECASE)


def extract_size_from_text(text: str) -> str:
    size_str = re.search(size_pattern_litres, text)
    if size_str:
        size = size_str.group(0).replace(" L", "L")
    else:
        size_str = re.search(size_pattern_centimetres, text)
        if size_str:
            size = size_str.group(0)
        else:
            if "tree" in text.lower() or "crown" in text.lower():
                size = None
            elif text.lower() in ["small", "medium", "large"]:
                size = text.lower()
            else:
                print(f"Could not find size in {text}")
                size = None
    return size


def extract_price_from_text(price_str):
    return float(re.sub(r"[^\d.\.]", "", price_str))


def fetch_data_interactive(
    product_url: str, source_url: str, category: str, driver: webdriver
) -> list:
    """There are multiple options for this product. Hence we need to make a selection and come back to this one"""
    results = []

    driver.get(product_url)
    select_element = driver.find_element(
        By.XPATH, '//select[@class="form-select form-select--small"]'
    )
    select = Select(select_element)

    price = driver.find_element(
        By.XPATH, '//span[@class="price price--withTax"]'
    ).get_attribute("innerHTML")
    product_name = (
        driver.find_element(By.XPATH, '//h1[@class="productView-title"]')
        .get_attribute("innerHTML")
        .split(" - ")[0]
    )
    img_url = (
        driver.find_element(By.XPATH, '//div[@class="productView-img-container"]')
        .find_element(By.TAG_NAME, "img")
        .get_attribute("src")
    )
    try:
        description_lst = driver.find_element(
            By.XPATH, '//div[@id="custom-product-short-description"]'
        ).find_elements(By.TAG_NAME, "li")
        description = "\n".join(
            [element.get_attribute("innerHTML") for element in description_lst]
        )
    except AttributeError:
        description = (
            driver.find_element(
                By.XPATH, '//div[@id="custom-product-short-description"]'
            )
            .get_attribute("innerHTML")
            .strip()
        )

    for option in select_element.find_elements(By.TAG_NAME, "option"):
        option_value = option.get_attribute("value")
        option_name = option.get_attribute("innerHTML")
        if option_value == "" or option_name == "See Options":
            pass
        else:
            # Wait for the price element to change after making a selection
            select.select_by_value(option_value)
            try:
                WebDriverWait(driver, 5).until_not(
                    expected_conditions.text_to_be_present_in_element(
                        (By.XPATH, '//span[@class="price price--withTax"]'), price
                    )
                )
            except TimeoutException:
                print(f"timeout when fetching price for {option_name}")

            price = driver.find_element(
                By.XPATH, '//span[@class="price price--withTax"]'
            ).get_attribute("innerHTML")
            try:
                stock = driver.find_element(
                    By.XPATH, '//span[@data-product-stock=""]'
                ).get_attribute("innerHTML")
                if stock == "":
                    stock = 1
            except NoSuchElementException:
                stock = 0

            price_inc_vat = extract_price_from_text(price)
            size = extract_size_from_text(option_name)
            quantity, multibuy = extract_quantity_from_text(option_name)
            results.append(
                {
                    "source": "quickcrop",
                    "source_url": source_url,
                    "product_url": product_url,
                    "category": category,
                    "product_name": product_name,
                    "product_code": None,
                    "img_url": img_url,
                    "description": description,
                    "price": price_inc_vat,
                    "size": size,
                    "stock": stock,
                    "quantity": quantity,
                    "multibuy": multibuy,
                }
            )
    return results


def fetch_data(
    product_url: str, source_url: str, category: str, session: HTMLSession
) -> dict:
    product_page = session.get(product_url)
    product_content = BeautifulSoup(product_page.content, "html.parser")

    product_name_str = product_content.find("h1", class_="productView-title").text
    product_name = product_name_str.split(" - ")[0]
    image = product_content.find("div", class_="productView-img-container").img
    img_url = image["src"]
    price_inc_vat_str = product_content.find("span", class_="price price--withTax").text
    price_inc_vat = extract_price_from_text(price_inc_vat_str)

    size = "9 cm"  # Size isn't specified so we default to 9cm

    quantity, multibuy = extract_quantity_from_text(product_name_str)

    try:
        stock = int(
            product_content.find(
                "div", class_="form-field form-field--stock"
            ).label.span.text
        )
        if stock == "":
            stock = 1
    except AttributeError:
        stock = 0

    try:
        description_lst = product_content.find(
            "div", id="custom-product-short-description"
        ).ul.find_all("li")
        description = "\n".join([element.text for element in description_lst])
    except AttributeError:
        description = product_content.find(
            "div", id="custom-product-short-description"
        ).text.strip()

    return {
        "source": "quickcrop",
        "source_url": source_url,
        "product_url": product_url,
        "category": category,
        "product_name": product_name,
        "product_code": None,
        "img_url": img_url,
        "description": description,
        "price": price_inc_vat,
        "size": size,
        "stock": stock,
        "quantity": quantity,
        "price_per_unit": round(price_inc_vat / quantity, 2),
        "multibuy": multibuy,
    }


def parse_url(URL: str, category: str, driver: webdriver) -> list[dict]:
    print(f"Fetching data for {category} from {URL}")
    session = HTMLSession()
    page_number = 1
    results = []

    while (page := session.get(f"{URL}?page={page_number}")).status_code == 200:
        content = BeautifulSoup(page.content, "html.parser")
        products = content.find("ul", class_="productGrid").find_all("li")

        for product in products:
            product_url = product.find("h2", class_="card-title").a["href"]

            price_inc_vat_str = product.find("span", class_="price price--withTax").text
            if "-" in price_inc_vat_str:
                # print(f"Parsing product(s) from URL {product_url} using selenium")
                results.extend(
                    fetch_data_interactive(
                        product_url=product_url,
                        source_url=URL,
                        category=category,
                        driver=driver,
                    )
                )
            else:
                # print(f"Parsing product from URL {product_url}")

                results.append(
                    fetch_data(
                        product_url=product_url,
                        source_url=URL,
                        category=category,
                        session=session,
                    )
                )
        page_number += 1

    print(f"Found {len(results)} products for {category}")

    return results


def get_product_data(config_file_name: str = "quickcrop") -> list[dict] | None:
    config = importlib.import_module("config." + config_file_name)
    results = []
    driver = selenium_setup()
    for URL, category in config.data_sources:
        results.extend(parse_url(URL=URL, category=category, driver=driver))
    driver.quit()
    return results
