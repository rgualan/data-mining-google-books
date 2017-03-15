import os
import logging
import requests
import mongo_handler
from logging import info, warning, error, debug
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
template_path = "input/template.json"


def crawl_metadata(folder_name):
    info("Processing {}".format(folder_name))

    book_id = folder_name[4:]  # discard the prefix

    url = "https://books.google.co.uk/books?id={}".format(book_id)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    metadata_table = soup.find("table", {"id":"metadata_content_table"})

    if not metadata_table:  # metadata table was not found
        warning("Metadata table was not found for book id {}".format(book_id))
        return []

    metadata = []
    for table_row in metadata_table.find_all("tr"):
        a_label = table_row.find("td", {"class": "metadata_label"})
        if a_label and "Citation" not in a_label.text:
            label = a_label.text
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
#mongo_handler.remove_metadata_collection()
parse_collection("input/gap-html")
