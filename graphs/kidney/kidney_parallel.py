import networkx as nx
import random
import argparse
from tqdm import tqdm
import psutil
from multiprocessing import Pool

# Function to randomly assign blood types to vertices based on provided probabilities
def assign_blood_type(probabilities):
    return random.choices(list(probabilities.keys()), list(probabilities.values()))[0]

# Function to check blood type compatibility
def are_compatible(blood_type1, blood_type2):
    if blood_type1 == 'O' or blood_type2 == 'O':
        return True
    elif blood_type1 == 'AB' or blood_type2 == 'AB':
        return True
    elif blood_type1 == blood_type2:
        return True
    return False

# Determine the number of processes based on the number of threads available
threads_count = psutil.cpu_count(logical=False)
num_processes = max(1, int(threads_count))

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate a graph with specified number of vertices, edges, and output file name.')
parser.add_argument('-N', type=int, default=100, help='Number of vertices')
parser.add_argument('-M', type=int, default=150, help='Number of edges')
parser.add_argument('--O_prob', type=int, default=50, help='Probability of blood type O (in integer form)')
parser.add_argument('--A_prob', type=int, default=30, help='Probability of blood type A (in integer form)')
parser.add_argument('--B_prob', type=int, default=15, help='Probability of blood type B (in integer form)')
parser.add_argument('--AB_prob', type=int, default=5, help='Probability of blood type AB (in integer form)')
parser.add_argument('-output', type=str, default=None, help='Output file name')
args = parser.parse_args()

# Convert integer probabilities to float probabilities (dividing by 100)
o_prob = args.O_prob / 100.0
a_prob = args.A_prob / 100.0
b_prob = args.B_prob / 100.0
ab_prob = args.AB_prob / 100.0

# Define the blood type probabilities based on command-line arguments
blood_type_probs = {
    'O': o_prob,
    'A': a_prob,
    'B': b_prob,
    'AB': ab_prob,
}

# Create an empty graph
G = nx.Graph()

# Add N vertices with assigned blood types to the graph
for i in range(args.N):
    blood_type = assign_blood_type(blood_type_probs)
    G.add_node(i, blood_type=blood_type)

# Add edges until M edges are added (capitalized)
edges_per_process = args.M // num_processes

# Create edge chunks for parallel processing
edge_chunks = []
for _ in range(num_processes):
    edge_chunk = random.sample(G.nodes(), edges_per_process * 2)  # Sample twice as many nodes
    edge_chunk = [(edge_chunk[i], edge_chunk[i+1]) for i in range(0, len(edge_chunk), 2)]  # Create pairs
    edge_chunks.append(edge_chunk)

# Function to add edges in parallel
def add_edges_parallel(args):
    chunk, node_blood_types, p = args
    result = []
    for u, v in chunk:
        blood_type_u = node_blood_types[u]
        blood_type_v = node_blood_types[v]
        if are_compatible(blood_type_u, blood_type_v) or random.random() <= p:
            result.append((u, v))
    return result

# Add edges in parallel without progress bars
with Pool(num_processes) as pool:
    result_edges = pool.map(add_edges_parallel, [(chunk, nx.get_node_attributes(G, 'blood_type'), 0.2) for chunk in edge_chunks])

# Flatten the list of edge lists
edges_to_add = [edge for sublist in result_edges for edge in sublist]

# Add the edges to the graph
G.add_edges_from(edges_to_add)

# Default output file name includes N, M, and blood type probabilities (capitalized)
# Generate the output file name only if no output argument is provided
if args.output is None:
    output_file = f"blood_type_graph_N{args.N}_M{args.M}_O{args.O_prob}_A{args.A_prob}_B{args.B_prob}_AB{args.AB_prob}.txt"
else:
    output_file = args.output

# Create a tqdm progress bar for sequential edge generation
with tqdm(total=args.M, desc="Edges generated") as pbar_total:
    # Write the edge list to the specified output file and update the progress bar
    with open(output_file, "w") as file:
        # Write the header lines for the original format
        file.write(f"vertices {args.N}\n")
        file.write(f"edges {G.number_of_edges()}\n")

        # Write each edge with the "edge" prefix, adding 1 to each vertex
        for edge in G.edges():
            u, v = edge
            file.write(f"edge {u + 1} {v + 1}\n")
            pbar_total.update(1)

    # If matrix_market_format is True, write the Matrix Market format to a separate file
    matrix_market_format = True
    if matrix_market_format:
        matrix_market_file = output_file + ".mtx"
        with open(matrix_market_file, "w") as mm_file:
            mm_file.write("%%MatrixMarket matrix coordinate pattern symmetric\n")
            mm_file.write(f"{args.N} {args.N} {G.number_of_edges()}\n")
            for edge in G.edges():
                u, v = edge
                mm_file.write(f"{u + 1} {v + 1}\n")
                pbar_total.update(1)

# Print the number of connected components
num_connected_components = nx.number_connected_components(G)
print(f"Number of connected components: {num_connected_components}")

print(f"Random kpd graph with {args.N} vertices and {G.number_of_edges()} edges (vertices incremented by 1) written to {output_file}.")

