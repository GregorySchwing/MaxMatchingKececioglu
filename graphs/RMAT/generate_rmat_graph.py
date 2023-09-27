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
print(sys.argv,len(sys.argv),sys.argv[6].lower())
if len(sys.argv) == 8 and sys.argv[7].lower() == "true":
    calculate_triangles = True
    print("Calc triangles")

# Generate an RMAT graph using cuGraph
G_cugraph = rmat(num_vertices, num_edges, a, b, c)

# Calculate centrality measures if requested
if calculate_triangles:
    alpha = 0.1  # Adjust as needed
    calculate_centrality_and_triangles(G_cugraph, output_file)

# Write the edge list to the file
write_edge_list(G_cugraph, output_file)

