import sys
import os
import pandas as pd
import cugraph as cnx
import cudf
import networkx as nx
import random

# Set the random seed for reproducibility
random.seed(123)

if len(sys.argv) != 5:
    print("Usage: python generate_watts_strogatz_graph.py <num_vertices> <k> <p> <output_file>")
    sys.exit(1)

num_vertices = int(sys.argv[1])
k = int(sys.argv[2])
p = float(sys.argv[3])  # Probability of rewiring each edge
output_file = sys.argv[4]

# Generate a Watts-Strogatz small-world graph using NetworkX
G_networkx = nx.watts_strogatz_graph(num_vertices, k, p, seed=123)

# Convert the NetworkX edge list to a cuGraph graph
edges_df = pd.DataFrame(list(G_networkx.edges), columns=["src", "dst"])
G_cugraph = cnx.from_pandas_edgelist(edges_df, source="src", destination="dst")

# Calculate degree centrality using cuGraph
degree_centrality = cnx.degree(G_cugraph)

# Calculate betweenness centrality using cuGraph
betweenness_centrality = cnx.betweenness_centrality(G_cugraph)

# Calculate closeness centrality using cuGraph
closeness_centrality = cnx.closeness_centrality(G_cugraph)

# Calculate eigenvector centrality using cuGraph
eigenvector_centrality = cnx.eigenvector_centrality(G_cugraph)

# Calculate clustering coefficient using NetworkX
clustering_coefficient = nx.average_clustering(G_networkx)

# Extract the base filename without extension by joining command-line arguments with underscores
base_filename = "_".join(sys.argv[1:4])

# Create the output filename with the base filename and .csv extension
output_filename = f"{base_filename}.csv"

# Create or append to the log CSV file
log_columns = ["Vertices", "Edges", "Arguments", "ClusteringCoefficient", "DegreeCentrality", "BetweennessCentrality", "ClosenessCentrality", "EigenvectorCentrality"]

if os.path.isfile("log.csv"):
    log_df = pd.read_csv("log.csv")
else:
    log_df = pd.DataFrame(columns=log_columns)

log_df = log_df.append({
    "Vertices": num_vertices,
    "Edges": G_cugraph.number_of_edges,
    "Arguments": " ".join(sys.argv[1:]),
    "ClusteringCoefficient": clustering_coefficient,
    "DegreeCentrality": degree_centrality,
    "BetweennessCentrality": betweenness_centrality,
    "ClosenessCentrality": closeness_centrality,
    "EigenvectorCentrality": eigenvector_centrality,
}, ignore_index=True)

log_df.to_csv("log.csv", index=False)

print(f"Watts-Strogatz small-world graph with {num_vertices} vertices and {G_cugraph.number_of_edges} edges (vertices incremented by 1) written to {output_filename}.")

