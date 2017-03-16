import mongo_handler


def parse_book(book_metadata):
    book = dict()

    book["book_id"] = book_metadata["book_id"]

    for bm in book_metadata["metadata"]:
        if bm["label"] == "Title":
            book["title"] = bm["value"]
        elif bm["label"] == "Author":
            book["author"] = bm["value"]
        elif bm["label"] == "Translated by":
            book["translator"] = bm["value"]
        elif bm["label"] == "Publisher":
            book["publisher"] = bm["value"]

    return book


def print_metadata():
    books_metadata = mongo_handler.query_metadata()

    for bm in books_metadata:
        bo = parse_book(bm)
        print("{}\t{}\t{}\t{}".format(
            bo["book_id"],
            bo["title"] if "title" in bo else "",
            bo["author"] if "author" in bo else "",
            bo["translator"] if "translator" in bo else ""
        ))


def append_metadata(book):
    metadata = mongo_handler.query_metadata_entry(book["book_id"])

    if not metadata:
        return

    bo = parse_book(metadata)

    book["title"] = bo["title"] if "title" in bo else ""
    book["author"] = bo["author"] if "author" in bo else ""
    book["translator"] = bo["translator"] if "translator" in bo else ""


if __name__ == "__main__":
    print_metadata()
