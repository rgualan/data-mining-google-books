import os
import json
import mongo_handler
from os.path import basename
from local_constant import *


def read_books_one_by_one():
    directory = EXTRACTION_FOLDER
    print("Reading collection from {}".format(directory))

    names = []
    books = []
    for file_name in os.listdir(directory):
        folder_path = os.path.join(directory, file_name)

        name = os.path.splitext(basename(folder_path))[0]
        names.append(name)

        with open(folder_path) as data_file:
            book = json.load(data_file)
            books.append(book["content"])

    return books, names


def read_books_from_compiled_collection():
    input_file = EXTRACTION_COMPILED_FILE
    print("Reading collection from {}".format(input_file))

    with open(input_file) as data_file:
        return json.load(data_file)


def read_books_from_mongo():
    return mongo_handler.query_books()


def extract_corpus(books):
    """
    Returns a list of strings, where each string is the content of the book
    :param books: list of book entities
    :return: list of contents
    """
    contents = []
    for book in books:
        contents.append(book["content"])

    return contents


def read_books_corpus():
    books = read_books_from_mongo()
    return extract_corpus(books)


def read_books():
    """
    Reads the books entities from the most convenient source (file or Mongo)
    :return: a list of books
    """
    return read_books_from_compiled_collection()