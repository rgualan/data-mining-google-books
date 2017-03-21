from logging import info, warning

import requests
from bs4 import BeautifulSoup

from util import mongo_handler


def crawl_metadata(book):
    info("Processing {}".format(book["book_id"]))

    book_id2 = book["book_id"][4:]  # discard the prefix
    book["book_id2"] = book_id2

    url = "https://books.google.co.uk/books?id={}".format(book_id2)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    metadata_table = soup.find("table", {"id": "metadata_content_table"})

    if not metadata_table:  # metadata table was not found
        warning("Metadata table was not found for book id {}".format(book_id2))
        return []

    for table_row in metadata_table.find_all("tr"):
        a_label = table_row.find("td", {"class": "metadata_label"})
        if a_label and "Citation" not in a_label.text:
            label = a_label.text
            value = table_row.find("td", {"class": "metadata_value"}).text
            if label == "Title":
                book["title"] = value
            elif label == "Author":
                book["author"] = value
            elif label == "Translated by":
                book["translator"] = value
            elif label == "Publisher":
                book["publisher"] = value

        # Special considerations
        if not book["author"] and book["translator"]:
            book["author"] = book["translator"]

    return book


def crawl_metadata_for_collection():
    books = mongo_handler.query_books()

    updated_books = []
    rec_number = 1
    for book in books:
        book["book_id3"] = str(rec_number)
        rec_number += 1
        book = crawl_metadata(book)
        updated_books.append(book)

    # Drop collection and insert new data
    mongo_handler.remove_book_collection()
    mongo_handler.insert_books(updated_books)


def group_books_by_author(books):
    """
    Aggregate books by author
    :param books:
    :return:
    """
    books_by_author = dict()
    books_no_author = []
    for book in books:
        if book["author"]:
            if book["author"] not in books_by_author:
                books_by_author[book["author"]] = [book["book_id3"]]
            else:
                books_by_author[book["author"]].append(book["book_id3"])
        else:
            books_no_author.append(book["book_id3"])

    return books_by_author, books_no_author


def build_link_ids(book1, book2):
    link_ids = list()
    link_ids.append("{}#{}".format(book1["book_id3"], book2["book_id3"]))
    link_ids.append("{}#{}".format(book2["book_id3"], book1["book_id3"]))
    return link_ids


def count_coincidences(book1, book2):
    count = 0
    for w in book1["top10words"]:
        if w in book2["top10words"]:
            count += 1
    return count


def calc_link_weights(books):
    links = dict()
    for b1 in books:
        for b2 in books:
            link_id = build_link_ids(b1, b2)
            if b1 != b2 and not (link_id[0] in links or link_id[1] in links):
                links[link_id[0]] = count_coincidences(b1, b2)
    return links


def print_metadata():
    books = mongo_handler.query_books()

    # Print all books
    i = 1
    for book in books:
        print("{}\t{}\t{}\t<{}>\t<{}>\t<{}>\t<{}>"
              .format(i,
                      book["book_id"],
                      book["book_id2"],
                      book["title"][:25] + '(...)',
                      book["author"],
                      book["translator"],
                      book["publisher"] if "publisher" in book and book["publisher"] else ""
                      ))
    print()

    # # How many books with author?
    # books_with_author = [b for b in books if "author" in book and len(book["author"])>0]
    # print("Books with author: {}".format(len(books_with_author)))

    # Aggregate books by author
    books_by_author, books_no_author = group_books_by_author(books)
    print("Books by author:")
    for author, subgroup in books_by_author.items():
        print("{}: {}".format(author, subgroup))
    print("Books without author: {}".format(books_no_author))
    print()


# Main
if __name__ == "__main__":
    # crawl_metadata_for_collection()
    print_metadata()
