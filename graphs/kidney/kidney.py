import networkx as nx
import random
import argparse
from tqdm import tqdm

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
with tqdm(total=args.M) as pbar:
    while G.number_of_edges() < args.M:
        # Randomly choose two vertices
        u, v = random.sample(G.nodes(), 2)

        # Get the blood types of the selected vertices
        blood_type_u = G.nodes[u]['blood_type']
        blood_type_v = G.nodes[v]['blood_type']

        # Check if the blood types are compatible
        if are_compatible(blood_type_u, blood_type_v):
            G.add_edge(u, v)
            pbar.update(1)  # Update the status bar
        else:
            # Add an edge with probability p = 0.2
            if random.random() <= 0.2:
                G.add_edge(u, v)
                pbar.update(1)  # Update the status bar

# Default output file name includes N, M, and blood type probabilities (capitalized)
# Generate the output file name only if no output argument is provided
if args.output is None:
    output_file = f"blood_type_graph_N{args.N}_M{args.M}_O{args.O_prob}_A{args.A_prob}_B{args.B_prob}_AB{args.AB_prob}.txt"
else:
    output_file = args.output


# Write the edge list to the specified output file
with open(output_file, "w") as file:
    # Write the header lines for the original format
    file.write(f"vertices {args.N}\n")
    file.write(f"edges {G.number_of_edges()}\n")

    # Write each edge with the "edge" prefix, adding 1 to each vertex
    for edge in G.edges():
        u, v = edge
        file.write(f"edge {u + 1} {v + 1}\n")

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

    print(f"Matrix Market format written to {matrix_market_file}.")

print(f"Random kpd graph with {args.N} vertices and {G.number_of_edges()} edges (vertices incremented by 1) written to {output_file}.")

