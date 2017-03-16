import json
import time
from logging import warning
from pymongo import MongoClient

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'googlebooks'
METADATA = 'book_metadata'
BOOK = 'book'


def remove_metadata_collection():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][METADATA]

    # Drop table (if exists)
    if METADATA in connection[DBS_NAME].collection_names():  # Check if collection exists in db
        if collection.count() > 0:  # Check if collection is not empty
            print('Dropping old collection...')
            collection.drop()  # Delete(drop) collection named from db

    connection.close()


def remove_book_collection():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][BOOK]

    # Drop table (if exists)
    if BOOK in connection[DBS_NAME].collection_names():  # Check if collection exists in db
        if collection.count() > 0:  # Check if collection is not empty
            print('Dropping old collection...')
            collection.drop()  # Delete(drop) collection named from db

    connection.close()


def insert_metadata(metadata):
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][METADATA]
    collection.insert(metadata)

    connection.close()


def insert_books(books):
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][BOOK]
    collection.insert(books)

    connection.close()


def query_metadata():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][METADATA]

    find_result = collection.find()

    metadata = []
    if find_result:
        metadata = list(find_result)

    connection.close()
    return metadata


def query_metadata_entry(book_id):
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][METADATA]

    metadata = collection.find_one({'book_id': book_id})

    if not metadata:
        warning("Metadata not found for book: %s", book_id)

    connection.close()
    return metadata


def query_books():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][BOOK]

    find_result = collection.find()

    books = []
    if find_result:
        books = list(find_result)

    connection.close()
    return books


def benchmark_reading_time():
    # Reading from file
    json_file = 'data/extracted/collection.json'
    print("Opening json file {}".format(json_file))
    st = time.time()

    with open(json_file) as data_file:
        books = json.load(data_file)
        print("Number of books: {}".format(len(books)))

    print("Time: {} ".format(time.time()-st))

    # Reading from MongoDB
    print("Querying books from mongo")
    st = time.time()

    with open(json_file) as data_file:
        books = json.load(data_file)
        print("Number of books: {}".format(len(books)))

    print("Time: {} ".format(time.time()-st))


if __name__ == "__main__":
    benchmark_reading_time()