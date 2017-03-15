import os
import re
import json
import logging
from logging import info, warning, error, debug
from datetime import datetime
from bs4 import BeautifulSoup
from html2json.html2json import extract, collect
from book_titles import BOOK_TITLES

logging.basicConfig(level=logging.INFO)
template_path = "input/template.json"


def parse_html_page(file_path):
    """
    Converts a file into a json object using the BeautifulSoup library
    :param file_path: the html file to parse
    :return: an object representing the page of a book
    """

    debug("Processing {}".format(file_path))

    # Read an html file
    file_data = open(file_path, 'r').read()  # returns a stream
    soup = BeautifulSoup(file_data, "html.parser")

    page = dict()
    page["title"] = soup.title.string
    page["numberOfPages"] = soup.find("meta", {"name": "ocr-number-of-pages"})["content"]

    pages = soup.find_all("div", {"class": "ocr_page"})
    debug("Number of pages {}".format(len(pages)))

    if len(pages) == 1:

        blocks = []
        for b in pages[0].find_all("div", {"class": "ocrx_block"}):
            debug("Block {}".format(b["title"]))
            block = dict()
            block["title"] = b["title"]

            paragraphs = []
            for p in b.find_all("p", {"class": "ocr_par"}):
                debug("Paragraph {}".format(p["title"]))
                paragraph = dict()
                paragraph["title"] = p["title"]

                lines = []
                for l in p.find_all("span", {"class": "ocr_line"}):
                    debug("Line {}".format(l["title"]))
                    line = dict()
                    line["title"] = l["title"]

                    words = []
                    for w in p.find_all("span", {"class": "ocr_cinfo"}):
                        debug("Word {}".format(w.string))
                        words.append(w.string)

                    line["words"] = words
                    lines.append(line)

                paragraph["lines"] = lines
                paragraphs.append(paragraph)

            block["paragraphs"] = paragraphs
            blocks.append(block)

        page["blocks"] = blocks
        return page

    elif len(pages) == 0:
        raise ValueError("Document {} has no pages!".format(file_path))
    elif len(pages) > 1:
        raise ValueError("Document {} has more than 1 page!".format(file_path))

    return page


def parse_html_page_simple(file_path):
    """
    Converts an html file into a json object using the BeautifulSoup library
    :param file_path: the html file to parse
    :return: an object representing the page of a book
    """

    debug("Processing {}".format(file_path))

    # Read an html file
    file_data = open(file_path, 'r').read()  # returns a stream
    soup = BeautifulSoup(file_data, "html.parser")

    page = dict()
    page["numberOfPages"] = soup.find("meta", {"name": "ocr-number-of-pages"})["content"]

    pages = soup.find_all("div", {"class": "ocr_page"})
    debug("Number of pages {}".format(len(pages)))

    if len(pages) == 1:

        content = pages[0].get_text()
        page["content"] = content

        return page

    elif len(pages) == 0:
        raise ValueError("Document {} has no pages!".format(file_path))
    elif len(pages) > 1:
        raise ValueError("Document {} has more than 1 page!".format(file_path))

    return page


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


def preprocessing_text(text):
    output = text
    # step-wise
    # output = re.sub(r'\d+', '', text)  # strip numbers
    # output = re.sub(r'\s+', ' ', output)  # strip white spaces
    # output = re.sub(r'[^a-zA-Z0-9 ]+', '', output)  # strip non-alphanumeric
    output = output.lower()  # normalize
    output = re.sub(r'\b\w{1,2}\b', '', output)  # strip small words (less than a threshold)

    tokens = re.split(r'[^A-Z^a-z]+', output)  # tokenize based on data mining slides
    #tokens = nltk.word_tokenize(output)  # tokenize

    # stop words
    stop = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop]

    # stemmer
    porter = nltk.PorterStemmer()  # stemmer (Problem: iing)
    try:
        tokens = [porter.stem(t) for t in tokens]
    except:  # catch *all* exceptions
        pass

    # lemmanization
    wnl = nltk.WordNetLemmatizer()
    tokens = [wnl.lemmatize(t) for t in tokens]

    # join tokens
    output = " ".join(tokens)

    return output


def parse_book(folder):
    info("Parsing book from {}".format(folder))

    book = dict()
    book["source"] = folder
    folder_name = os.path.splitext(os.path.basename(folder))[0]
    book["title"] = BOOK_TITLES[folder_name]

    content = ""
    page_count = 0
    for filename in os.listdir(folder):
        if filename.endswith(".html"):
            file_path = os.path.join(folder, filename)

            page = parse_html_page_simple(file_path)
            content = content + page["content"]
            page_count = page_count + 1

    book["numberOfPages"] = page_count

    book["content"] = preprocessing_text(content)

    return book


def parse_book_2(directory):
    info("Parsing book from {}".format(directory))

    pages = []

    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            file_path = os.path.join(directory, filename)

            pageJson = parse_html_page(file_path)
            pageJson["cid"] = "{}-{}".format(directory, filename)
            pages.append(pageJson)

    return pages


def parse_collection(directory):
    info("Parsing collection from {}".format(directory))
    books = []

    for foldername in os.listdir(directory):
        folder_path = os.path.join(directory, foldername)

        book = parse_book(folder_path)
        books.append(book)

    return books


def parse_collection_2(directory):
    info("Parsing collection from {}".format(directory))

    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)

        book = parse_book(folder_path)

        output_file = os.path.join("output/json-text-only-2", folder_name + ".json")
        info("Saving file {}".format(output_file))
        with open(output_file, 'w') as fp:
            json.dump(book, fp)


# Page
# page = parse_html_page('input/gap-html/gap_2X5KAAAAYAAJ/00000065.html')
# page = parse_html_page_simple('input/gap-html/gap_2X5KAAAAYAAJ/00000065.html')
# print(page)
# with open('output/book-page.json', 'w') as fp:
#    json.dump(page, fp)

# Book
# book = parse_book('input/gap-html/gap_2X5KAAAAYAAJ')
# print(book)
# with open('output/book.json', 'w') as fp:
#    json.dump(book["pages"], fp)

# Collection of books
# pages = parse_book_2('input/gap-html/gap_2X5KAAAAYAAJ')
# print(book)
# with open('output/book-pages.json', 'w') as fp:
#    json.dump(pages, fp)

parse_collection_2("input/gap-html")
