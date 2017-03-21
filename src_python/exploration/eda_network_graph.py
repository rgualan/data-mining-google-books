import matplotlib.pyplot as plt
import networkx as nx

import util.mongo_handler as mongo_handler
from extraction import metadata_handler

colors = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3',
          '#fdb462', '#b3de69', '#fccde5', '#d9d9d9']

if __name__ == "__main__":
    books = mongo_handler.query_books_2()
    books_by_author, books_no_author = metadata_handler.group_books_by_author(books)
    links = metadata_handler.calc_link_weights(books)  # Calculate the link weights
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

    min_matches = 1
    thresshold = 4

    for link_id in links:
        b1 = link_id.split("#")[0]
        b2 = link_id.split("#")[1]
        if links[link_id] > min_matches:
            G.add_edge(b1, b2, weight=links[link_id])

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > thresshold]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= thresshold]

    # nodes
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx_nodes(G, pos,
                           nodelist=books_no_author,
                           node_size=500, node_color='#FFFF00')

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
