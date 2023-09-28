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

def are_pair_compatible(pair1, pair2):
    person11, person12 = pair1  # First person in the first pair and second person in the first pair
    person21, person22 = pair2  # First person in the second pair and second person in the second pair

    # Check compatibility based on your criteria
    compatible_case1 = are_compatible(person11, person21) and are_compatible(person12, person22)
    compatible_case2 = are_compatible(person11, person22) and are_compatible(person12, person21)

    return compatible_case1 or compatible_case2

# Define the pair_compatible function
def pair_compatible_index(successful_pairs, pair1_index, pair2_index):
    pair1 = successful_pairs[pair1_index]
    pair2 = successful_pairs[pair2_index]

    person1_a, person1_b = pair1
    person2_a, person2_b = pair2
    
    # Check compatibility in both ways
    compatible1 = are_compatible(person1_a, person2_a) and are_compatible(person1_b, person2_b)
    compatible2 = are_compatible(person1_a, person2_b) and are_compatible(person1_b, person2_a)
    
    return compatible1 or compatible2

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
    edge_chunk = random.choices(list(G.nodes()), k=edges_per_process * 2)  # Sample with replacement
    edge_chunk = [(edge_chunk[i], edge_chunk[i + 1]) for i in range(0, len(edge_chunk), 2)]  # Create pairs
    edge_chunks.append(edge_chunk)

# Function to add edges in parallel
def evaluate_pairs(args):
    N, blood_types, compatibility_threshold, probability_pc = args
    num_samples = 2 * N // num_processes  # Sample N/number of processes pairs
    pairs_to_evaluate = random.choices(blood_types, k=num_samples)  # Sample blood types

    successful_pairs = []
    for i in range(0, len(pairs_to_evaluate), 2):
        blood_type_u, blood_type_v = pairs_to_evaluate[i], pairs_to_evaluate[i + 1]
        if not are_compatible(blood_type_u, blood_type_v) or random.uniform(0, 1) <= compatibility_threshold:
            successful_pairs.append((blood_type_u, blood_type_v))
    return successful_pairs

result_vertices = []  # Changed variable name

# Keep running until the length of result_vertices > N
while len(result_vertices) <= args.N:  # Changed variable name
    # Add edges in parallel without progress bars
    with Pool(num_processes) as pool:
        result_edges_batch = pool.map(evaluate_pairs, [(args.N, nx.get_node_attributes(G, 'blood_type'), 0.2, 0.2) for _ in range(num_processes)])

    # Flatten the list of edge lists and extend the result_vertices list
    edges_batch = [edge for sublist in result_edges_batch for edge in sublist]
    result_vertices.extend(edges_batch)  # Changed variable name

# Remove extra edges if more than N edges were generated
result_vertices = result_vertices[:args.N]  # Changed variable name

from itertools import combinations_with_replacement, islice, tee

n_processes = num_processes
n = args.N  # num cols/rows in matrix

pairs = ((i, j) for i, j in combinations_with_replacement(range(n), 2) if i != j)
pair_chunks = [
    list(islice(p, i, None, n_processes))
    for i, p in enumerate(tee(pairs, n_processes))
]

print(pair_chunks)
quit()
# Add the edges to the graph
G.add_edges_from(result_vertices)  # Changed variable name

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
