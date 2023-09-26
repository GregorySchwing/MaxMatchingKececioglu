import sys
import networkx as nx
import random
import pandas as pd
import matplotlib.pyplot as plt
import cugraph as cnx
import cudf

# Set the random seed for reproducibility
random.seed(123)

if len(sys.argv) != 5:
    print("Usage: python generate_newman_watts_strogatz_graph.py <num_vertices> <k> <p> <output_file>")
    sys.exit(1)

num_vertices = int(sys.argv[1])
k = int(sys.argv[2])
p = float(sys.argv[3])  # Probability of rewiring each edge
output_file = sys.argv[4]

# Generate a connected Watts-Strogatz small-world graph using NetworkX
G_networkx = nx.watts_strogatz_graph(num_vertices, k, p, seed=123)

# Convert the NetworkX graph to a cuGraph graph
G_cugraph = cnx.Graph()
G_cugraph.from_networkx(G_networkx)

# Calculate the clustering coefficient using cuGraph
clustering_coefficient = cnx.clustering_coefficient(G_cugraph)

# Calculate the average path length using NetworkX
average_path_length = nx.average_shortest_path_length(G_networkx)

# Get the degree distribution
degree_distribution = dict(nx.degree(G_networkx))

# Write the edge list to the file with the specified format
with open(output_file, "w") as file:
    # Write the header lines
    file.write(f"vertices {num_vertices}\n")
    file.write(f"edges {G_cugraph.number_of_edges}\n")
    
    # Write each edge with the "edge" prefix, adding 1 to each vertex
    for edge in G_cugraph.view_edge_list().to_pandas().itertuples(index=False):
        file.write(f"edge {edge[0] + 1} {edge[1] + 1}\n")

# Append information to the log file
log_file_name = "log.txt"  # You can change the log file name as needed
with open(log_file_name, "a") as log_file:
    log_file.write(f"Output file: {output_file}\n")
    log_file.write(f"Command-line arguments: {sys.argv}\n")
    log_file.write(f"Clustering coefficient: {clustering_coefficient}\n")
    log_file.write(f"Average path length: {average_path_length}\n")

print(f"Watts-Strogatz small-world graph with {num_vertices} vertices

