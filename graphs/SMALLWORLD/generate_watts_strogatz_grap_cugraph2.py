import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
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

# Calculate the clustering coefficient using cuGraph
clustering_coefficient = cnx.clustering_coefficient(G_cugraph)

# Calculate the average shortest path length using NetworkX
average_path_length = nx.average_shortest_path_length(G_networkx)

# Get the degree distribution
degree_distribution = dict(nx.degree(G_networkx))

# Extract the base filename without extension by joining command-line arguments with underscores
base_filename = "_".join(sys.argv[1:4])

# Create the output filename with the base filename and .csv extension
output_filename = f"{base_filename}.csv"

# Write the edge list to the file with the specified format
with open(output_filename, "w") as file:
    # Write the header lines
    file.write(f"vertices {num_vertices}\n")
    file.write(f"edges {G_cugraph.number_of_edges}\n")
    
    # Write each edge with the "edge" prefix, adding 1 to each vertex
    for edge in G_cugraph.view_edge_list().to_pandas().itertuples(index=False):
        file.write(f"edge {edge[0] + 1} {edge[1] + 1}\n")

# Append information to the log file
log_file_name = "log.txt"  # You can change the log file name as needed
with open(log_file_name, "a") as log_file:
    log_file.write(f"Output file: {output_filename}\n")
    log_file.write(f"Command-line arguments: {sys.argv}\n")
    log_file.write(f"Clustering coefficient: {clustering_coefficient}\n")
    log_file.write(f"Average path length: {average_path_length}\n")

print(f"Watts-Strogatz small-world graph with {num_vertices} vertices and {G_cugraph.number_of_edges} edges (vertices incremented by 1) written to {output_filename}.")

# Save average path length to a CSV file with input filename + _average_path_length.csv
avg_path_length_file = f"{base_filename}_average_path_length.csv"
avg_path_length_df = pd.DataFrame({"Average Path Length": [average_path_length]})
avg_path_length_df.to_csv(avg_path_length_file, index=False)

# Save degree distribution to a CSV file with input filename + _degree_distribution.csv
degree_distribution_file = f"{base_filename}_degree_distribution.csv"
degree_distribution_df = pd.DataFrame(degree_distribution.items(), columns=["Node", "Degree"])
degree_distribution_df.to_csv(degree_distribution_file, index=False)

# Plot and save the degree distribution as a line graph
plt.bar(degree_distribution.keys(), degree_distribution.values())
plt.xlabel("Node Degree")
plt.ylabel("Frequency")
plt.title("Degree Distribution")
plt.savefig("degree_distribution.png")
plt.show()

