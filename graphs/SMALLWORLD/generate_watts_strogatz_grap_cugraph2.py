import sys
import os
import pandas as pd
import cugraph
import cudf
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt

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
G_cugraph = cugraph.Graph()
G_cugraph.from_cudf_edgelist(cudf.from_pandas(edges_df), source="src", destination="dst")

# Calculate degree centrality using cuGraph
degree_centrality = cugraph.centrality.degree_centrality(G_cugraph)

# Calculate betweenness centrality using cuGraph
betweenness_centrality = cugraph.centrality.betweenness_centrality(G_cugraph)

# Calculate closeness centrality using cuGraph
closeness_centrality = cugraph.centrality.closeness_centrality(G_cugraph)

# Calculate eigenvector centrality using cuGraph
eigenvector_centrality = cugraph.centrality.eigenvector_centrality(G_cugraph)

# Calculate Katz centrality using cuGraph
alpha = 0.1  # Adjust as needed
katz_centrality = cugraph.centrality.katz_centrality(G_cugraph, alpha=alpha)

# Calculate clustering coefficient using NetworkX
clustering_coefficient = nx.average_clustering(G_networkx)

# Calculate the number of triangles
triangles = cugraph.triangle_count(G_cugraph)

# Calculate the average centrality measures
avg_degree_centrality = degree_centrality.mean()
avg_betweenness_centrality = betweenness_centrality.mean()
avg_closeness_centrality = closeness_centrality.mean()
avg_eigenvector_centrality = eigenvector_centrality.mean()
avg_katz_centrality = katz_centrality.mean()

# Extract the base filename without extension by joining command-line arguments with underscores
base_filename = "_".join(sys.argv[1:4])

# Create or append to the log CSV file
log_columns = ["Vertices", "Edges", "Arguments", "ClusteringCoefficient", "AverageDegreeCentrality", "AverageBetweennessCentrality", "AverageClosenessCentrality", "AverageEigenvectorCentrality", "AverageKatzCentrality", "TriangleCount"]

if os.path.isfile("log.csv"):
    log_df = pd.read_csv("log.csv")
else:
    log_df = pd.DataFrame(columns=log_columns)

log_df = log_df.append({
    "Vertices": num_vertices,
    "Edges": G_cugraph.number_of_edges(),
    "Arguments": " ".join(sys.argv[1:]),
    "ClusteringCoefficient": clustering_coefficient,
    "AverageDegreeCentrality": avg_degree_centrality,
    "AverageBetweennessCentrality": avg_betweenness_centrality,
    "AverageClosenessCentrality": avg_closeness_centrality,
    "AverageEigenvectorCentrality": avg_eigenvector_centrality,
    "AverageKatzCentrality": avg_katz_centrality,
    "TriangleCount": triangles,
}, ignore_index=True)

log_df.to_csv("log.csv", index=False)

# Create histograms and save histogram data to CSV files
def save_histogram_data(centrality_values, centrality_name):
    histogram_data, bin_edges = np.histogram(centrality_values.to_array(), bins=20)
    histogram_df = pd.DataFrame({
        "BinEdges": bin_edges[:-1],
        "Frequency": histogram_data
    })
    histogram_df.to_csv(f"{base_filename}_{centrality_name}_histogram.csv", index=False)

save_histogram_data(degree_centrality, "DegreeCentrality")
save_histogram_data(betweenness_centrality, "BetweennessCentrality")
save_histogram_data(closeness_centrality, "ClosenessCentrality")
save_histogram_data(eigenvector_centrality, "EigenvectorCentrality")
save_histogram_data(katz_centrality, "KatzCentrality")

print("Watts-Strogatz small-world graph with {} vertices and {} edges (vertices incremented by 1) written to {}.".format(num_vertices, G_cugraph.number_of_edges(), output_file))

