import os
import re
import json
import logging
from logging import info, warning, error, debug
from datetime import datetime
from bs4 import BeautifulSoup
from html2json.html2json import extract, collect


DIRECTORY = "output/json-text-only-2"


def read_documents():
    directory = DIRECTORY
    info("Reading collection from {}".format(directory))

    books = []
    for file_name in os.listdir(directory):
        folder_path = os.path.join(directory, file_name)

        with open(folder_path) as data_file:
            book = json.load(data_file)
            books.append(book["content"])

    return books
