import os
import json
from datetime import datetime
from bs4 import BeautifulSoup
from html2json.html2json import extract, collect

template_path = "input/template.json"

# Converts a file into a json object using a template file (html2json)
def parse_html_page(file_path, template):
    # Read an html file
    file_data = open(file_path,'r').read() # returns a stream
    page = BeautifulSoup(file_data, "lxml") #
    #print(page)

    # Convert from html to json
    with open(template) as f:
        template = json.load(f)
        #print(template)
    data = collect(page, template)
    #data["fileName"] = "Some nanem"
    #data["crawlingDate"] = datetime.now().strftime("%B %-d, %Y")

    #print(data)
    #print(json.dumps(data, indent=4, sort_keys=True))

    return data

def parse_book(directory, template):
    book = dict()
    book["directorySource"] = directory
    book["pages"] = []

    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            #print(os.path.join(directory, filename))
            file_path = os.path.join(directory, filename)

            pageJson = parse_html_page(file_path, template)
            book["pages"].append(pageJson)

    #print(book)
    return book

def parse_collection(directory, template):
    books = []

    for foldername in os.listdir(directory):
        print("Processing book " + foldername)
        folder_path = os.path.join(directory, foldername)

        book = parse_book(folder_path, template)
        books.append(book)

    return books

# Main:
parse_html_page('input/gap-html/gap_2X5KAAAAYAAJ/00000065.html', template_path)

#book = parse_book('input/gap-html/gap_2X5KAAAAYAAJ', template_path)
#print(book)
#json.dump(book, "output/temp.json")

#books = parse_collection("input/gap-html", template_path);
#with open('output/collection.json', 'w') as outfile:
#    json.dump(books, outfile)
