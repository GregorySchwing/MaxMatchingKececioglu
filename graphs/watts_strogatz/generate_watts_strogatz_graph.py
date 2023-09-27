# generate_watts_strogatz_graph.py

import sys
import os
import networkx as nx
sys.path.insert(0, os.path.abspath('../utils'))  # Add the 'utils' directory to the Python path
from centrality_utils import calculate_centrality_and_triangles, write_edge_list

if len(sys.argv) < 5:
    print("Usage: python generate_watts_strogatz_graph.py <num_vertices> <k> <p> <output_file> [calculate_triangles]")
    sys.exit(1)

num_vertices = int(sys.argv[1])
k = int(sys.argv[2])
p = float(sys.argv[3])/10.0  # Probability of rewiring each edge
output_file = sys.argv[4]
calculate_triangles = False

if len(sys.argv) == 6 and sys.argv[5].lower() == "true":
    calculate_triangles = True

# Generate a Watts-Strogatz small-world graph using NetworkX
G_networkx = nx.watts_strogatz_graph(num_vertices, k, p, seed=123)

# Calculate centrality measures if requested
if calculate_triangles:
    alpha = 0.1  # Adjust as needed
    calculate_centrality_and_triangles(G_networkx, alpha, num_vertices, k, p, output_file)

# Write the edge list to the file
write_edge_list(G_networkx, output_file)

