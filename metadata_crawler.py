import os
import re
import json
import logging
import requests
import mongo_handler
from logging import info, warning, error, debug
from bs4 import BeautifulSoup
from book_titles import BOOK_TITLES
from pymongo import MongoClient

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'water_footprint'
COLLECTION_CROP_AGGREGATED = 'crop_products_aggregated_by_category'
COLLECTION_RECIPES = 'recipes_2'
COLLECTION_CROP = 'crop_products_by_category'
COLLECTION_INGREDIENT_TO_WATERFP = 'ingredient_to_waterfootprint'


logging.basicConfig(level=logging.INFO)
template_path = "input/template.json"


def crawl_metadata(folder_name):
    info("Processing {}".format(folder_name))

    book_id = folder_name[4:]

    url = "https://books.google.co.uk/books?id={}".format(book_id)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    metadata_table = soup.find("table", {"id":"metadata_content_table"})
    metadata = []
    for table_row in metadata_table.find_all("tr"):
        if table_row.find("td", {"class": "metadata_label"}):
            label = table_row.find("td", {"class": "metadata_label"}).text
            value = table_row.find("td", {"class": "metadata_value"}).text
            metadata.append([label, value])

    return metadata


def parse_collection(directory):
    info("Parsing collection from {}".format(directory))

    all_metadata = []
    for folder_name in os.listdir(directory):
        bm = dict()
        bm["book_id"] = folder_name
        bm["metadata"] = crawl_metadata(folder_name)
        all_metadata.append(bm)

    print("Saving metadata in MongoDB")
    mongo_handler.insert_metadata(all_metadata)

    print("Metadata: ")
    print(all_metadata)


# Main
parse_collection("input/gap-html")
