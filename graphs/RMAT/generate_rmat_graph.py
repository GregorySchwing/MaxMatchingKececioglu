# generate_rmat_graph.py

import sys
import os
import networkx as nx
import cugraph as cnx
from cugraph.generators import rmat
sys.path.insert(0, os.path.abspath('../utils'))  # Add the 'utils' directory to the Python path
from centrality_utils import calculate_centrality_and_triangles, write_edge_list

if len(sys.argv) < 6:
    print("Usage: python generate_rmat_graph.py <num_vertices> <num_edges> <a> <b> <c> <output_file> [calculate_triangles]")
    sys.exit(1)

num_vertices = int(sys.argv[1])
num_edges = int(sys.argv[2])
a = float(sys.argv[3])
b = float(sys.argv[4])
c = float(sys.argv[5])
d = 1.0 -a-b-c
output_file = sys.argv[6]
calculate_triangles = False

if len(sys.argv) == 7 and sys.argv[6].lower() == "true":
    calculate_triangles = True

# Generate an RMAT graph using cuGraph
G_cugraph = rmat(num_vertices, num_edges, a, b, c)

# Calculate centrality measures if requested
if calculate_triangles:
    alpha = 0.1  # Adjust as needed
    calculate_centrality_and_triangles(G_cugraph, alpha, num_vertices, k, p, output_file)

nx_graph = G_cugraph.to_networkx()
# Write the edge list to the file
write_edge_list(nx_graph, output_file)
