import os
import json
from os.path import basename
from book_titles import BOOK_TITLES

DIRECTORY = "output/json-text-only-2"


def read_documents():
    directory = DIRECTORY
    print("Reading collection from {}".format(directory))

    names = []
    titles = []
    books = []
    for file_name in os.listdir(directory):
        #print(file_name)
        folder_path = os.path.join(directory, file_name)
        #print(folder_path)

        #print(basename(folder_path))
        #print(os.path.splitext(basename(folder_path))[0])

        name = os.path.splitext(basename(folder_path))[0]
        names.append(name)
        titles.append(BOOK_TITLES[name])

        with open(folder_path) as data_file:
            book = json.load(data_file)
            books.append(book["content"])

    return books, titles, names

#_,titles,_ = read_documents()
#print(titles)