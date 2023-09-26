import sys
import pandas as pd
import matplotlib.pyplot as plt
import cugraph as cnx
import networkx as nx
import cudf

# Set the random seed for reproducibility
random_seed = 123
cnx.set_random_seed(random_seed)

if len(sys.argv) != 5:
    print("Usage: python generate_newman_watts_strogatz_graph.py <num_vertices> <k> <p> <output_file>")
    sys.exit(1)

num_vertices = int(sys.argv[1])
k = int(sys.argv[2])
p = float(sys.argv[3])  # Probability of rewiring each edge
output_file = sys.argv[4]

# Ensure k is greater than or equal to num_vertices
if k < num_vertices:
    k = num_vertices

# Generate a Watts-Strogatz small-world graph using cuGraph
G_cugraph = cnx.newman_watts_strogatz_graph(num_vertices, k, p, seed=123)

# Calculate the clustering coefficient using cuGraph
clustering_coefficient = cnx.clustering_coefficient(G_cugraph)

# Calculate the average shortest path length using cuGraph
avg_path_length = cnx.traversal.graph_sssp(G_cugraph)

# Convert cuGraph graph to a NetworkX graph for degree distribution
G_networkx = G_cugraph.view_edge_list().to_pandas().rename(columns={'src': 'source', 'dst': 'target'})
G_networkx = nx.from_pandas_edgelist(G_networkx)

# Get the degree distribution
degree_distribution = dict(G_networkx.degree())

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
    log_file.write(f"Average path length: {avg_path_length}\n")

print(f"Watts-Strogatz small-world graph with {num_vertices} vertices and {G_cugraph.number_of_edges} edges (vertices incremented by 1) written to {output_file}.")

# Save average path length to a CSV file
avg_path_length_df = pd.DataFrame({"Average Path Length": avg_path_length})
avg_path_length_df.to_csv("average_path_length.csv", index=False)

# Save degree distribution to a CSV file
degree_distribution_df = pd.DataFrame(degree_distribution.items(), columns=["Node", "Degree"])
degree_distribution_df.to_csv("degree_distribution.csv", index=False)

# Plot and save the degree distribution as a line graph
plt.bar(degree_distribution.keys(), degree_distribution.values())
plt.xlabel("Node Degree")
plt.ylabel("Frequency")
plt.title("Degree Distribution")
plt.savefig("degree_distribution.png")
plt.show()

