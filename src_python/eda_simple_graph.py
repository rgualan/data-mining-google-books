import matplotlib.pyplot as plt
import networkx as nx
import src_python.mongo_handler as mongo_handler


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


def calc_books_by_author(books):
    books_by_author = dict()
    books_no_author = []
    for book in books:
        if book["author"] and len(book["author"]) > 0:
            if book["author"] not in books_by_author:
                books_by_author[book["author"]] = [book["book_id3"]]
            else:
                books_by_author[book["author"]].append(book["book_id3"])
        else:
            books_no_author.append(book["book_id3"])

    return books_by_author, books_no_author


def calc_link_weights(books):
    links = dict()
    for b1 in books:
        for b2 in books:
            link_id = build_link_ids(b1, b2)
            if b1 != b2 and not (link_id[0] in links or link_id[1] in links):
                links[link_id[0]] = count_coincidences(b1, b2)
    return links


if __name__ == "__main__":
    books = mongo_handler.query_books_2()

    # Create custom id for the graph nodes
    print("Books:")
    for i in range(len(books)):
        books[i]["book_id3"] = "" + str(i)
        print("{}: {}".format(books[i]["book_id3"], books[i]["title"]))
    print()

    # Aggregate books by author
    books_by_author, books_no_author = calc_books_by_author(books)
    print("Books by author:")
    for author, subgroup in books_by_author.items():
        print("{}: {}".format(author, subgroup))
    print("Books without author: {}".format(books_no_author))
    print()

    links = calc_link_weights(books)  # Calculate the link weights
    max_weight = max(links.values())  # Calculate max link weight
    print("Max weight: {}".format(max_weight))

    # Print links
    log = sorted(["{}->{}".format(link, links[link]) for link in links])
    for l in log:
        print(l)
    print()

    # Draw the network
    G = nx.Graph()
    for book in books:
        G.add_node(book["book_id3"])

    for link_id in links:
        b1 = link_id.split("#")[0]
        b2 = link_id.split("#")[1]
        if links[link_id] > 1:
            G.add_edge(b1, b2, weight=links[link_id])

    thresshold = 4
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > thresshold]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= thresshold]

    pos = nx.spring_layout(G)  # positions for all nodes
    # nodes
    nx.draw_networkx_nodes(G, pos,
                           nodelist=books_no_author,
                           node_size=500, node_color='#d9d9d9')
    colors = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3',
              '#fdb462', '#b3de69', '#fccde5', '#d9d9d9']
    i = 0
    for subgroup in books_by_author.values():
        nx.draw_networkx_nodes(G, pos,
                               nodelist=subgroup,
                               node_size=500,
                               node_color=colors[i])
        i += 1

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=4, edge_color='g')
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=1, alpha=0.5, edge_color='g', style='dashed')

    # labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
    # nx.draw(G)
    plt.axis('off')
    plt.show()
