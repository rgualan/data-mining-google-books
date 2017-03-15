import logging
from pymongo import MongoClient

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'googlebooks'
METADATA = 'book_metadata'


def remove_metadata_collection():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    colMetadata = connection[DBS_NAME][METADATA]

    # Drop table (if exists)
    if METADATA in connection[DBS_NAME].collection_names():  # Check if collection exists in db
        if colMetadata.count() > 0:  # Check if collection is not empty
            print('Droping old collection...')
            colMetadata.drop()  # Delete(drop) collection named from db


def insert_metadata(metadata):
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    colMetadata = connection[DBS_NAME][METADATA]
    colMetadata.insert(metadata)



