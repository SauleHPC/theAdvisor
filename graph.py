import networkx as nx
import matplotlib.pyplot as plt
from pymongo import MongoClient
from bson.objectid import ObjectId

def create_graph():
    # Setup MongoDB connection
    client = MongoClient('localhost', 11111)
    db = client['theadvisor']  
    matches = db.theadvisor_papers  

    # Initialize a directed graph
    G = nx.DiGraph()

    # Fetch data from MongoDB
    for match in matches.find():
        mag_id = match['mag_id']
        dblp_id = match['dblp_id']
        G.add_node(mag_id, label='MAG', title=match.get('mag_title', 'No Title'))
        G.add_node(dblp_id, label='DBLP', title=match.get('dblp_title', 'No Title'))
        G.add_edge(mag_id, dblp_id, weight=1)

    return G

def draw_graph(G):
    pos = nx.spring_layout(G)  # positions for all nodes

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle='-|>', arrowsize=20, edge_color='c', style='dashed')
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_family='sans-serif')

    plt.axis('off')
    plt.savefig('/home/relhadid/image.png')  # Save the plot as a PNG file

if __name__ == "__main__":
    G = create_graph()
    draw_graph(G)
