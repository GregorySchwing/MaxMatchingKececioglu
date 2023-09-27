import os
import pandas as pd
import networkx as nx
import random
import matplotlib.pyplot as plt
try:
    import cugraph
    cugraph_available = True
except ImportError:
    cugraph_available = False

def calculate_centrality_and_triangles(G, num_vertices, num_edges, output_file):
    if cugraph_available:
        import cugraph
        import cudf

        # Calculate degree centrality using cuGraph
        degree_centrality = cugraph.centrality.degree_centrality(G)

        # Calculate betweenness centrality using cuGraph
        betweenness_centrality = cugraph.centrality.betweenness_centrality(G)

        # Calculate eigenvector centrality using cuGraph
        eigenvector_centrality = cugraph.centrality.eigenvector_centrality(G)

        # Calculate Katz centrality using cuGraph
        katz_centrality = cugraph.centrality.katz_centrality(G)
    else:
        # Calculate centrality measures using NetworkX
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)
        eigenvector_centrality = nx.eigenvector_centrality(G)
        katz_centrality = nx.katz_centrality(G)

    # Calculate clustering coefficient using NetworkX
    clustering_coefficient = 0
    # Calculate the number of triangles
    triangles = 0
    # Append to log file
    append_to_log_file(num_vertices, num_edges, output_file, clustering_coefficient,
                       degree_centrality, betweenness_centrality,
                       eigenvector_centrality, katz_centrality, triangles)

    # Save histogram data to CSV files
    save_histogram_data(degree_centrality, "DegreeCentrality", output_file)
    save_histogram_data(betweenness_centrality, "BetweennessCentrality", output_file)
    # save_histogram_data(closeness_centrality, "ClosenessCentrality", base_filename) # Removed
    save_histogram_data(eigenvector_centrality, "EigenvectorCentrality", output_file)
    save_histogram_data(katz_centrality, "KatzCentrality", output_file)

def append_to_log_file(num_vertices, num_edges, output_file, clustering_coefficient,
                       degree_centrality, betweenness_centrality,
                       eigenvector_centrality, katz_centrality, triangles):
    # Extract the base filename without extension
    base_filename = os.path.splitext(os.path.basename(output_file))[0]

    # Create or append to the log CSV file
    log_columns = ["Vertices", "Edges", "Arguments", "ClusteringCoefficient", "AverageDegreeCentrality",
                   "AverageBetweennessCentrality", "AverageEigenvectorCentrality",
                   "AverageKatzCentrality", "Triangles"]

    if os.path.isfile("log.csv"):
        log_df = pd.read_csv("log.csv")
    else:
        log_df = pd.DataFrame(columns=log_columns)

    log_df = log_df.append({
        "Vertices": num_vertices,
        "Edges": num_edges,
        "Basefile": f"{output_file}",
        "ClusteringCoefficient": clustering_coefficient,
        "AverageDegreeCentrality": sum(degree_centrality.values()) / len(degree_centrality),
        "AverageBetweennessCentrality": sum(betweenness_centrality.values()) / len(betweenness_centrality),
        "AverageEigenvectorCentrality": sum(eigenvector_centrality.values()) / len(eigenvector_centrality),
        "AverageKatzCentrality": sum(katz_centrality.values()) / len(katz_centrality),
        "Triangles": triangles
    }, ignore_index=True)

    log_df.to_csv("log.csv", index=False)

def save_histogram_data(centrality_values, centrality_name, output_file):
    histogram_data, bin_edges = np.histogram(list(centrality_values.values()), bins=20)
    histogram_df = pd.DataFrame({
        "BinEdges": bin_edges[:-1],
        "Frequency": histogram_data
    })
    histogram_df.to_csv(f"../utils/{output_file}_{centrality_name}_histogram.csv", index=False)

def write_edge_list(G, output_file):
    try:
        with open(output_file, 'w') as f:
            f.write(f"vertices {len(G.nodes)}\n")
            f.write(f"edges {len(G.edges)}\n")

            for edge in G.edges():
                f.write(f"edge {edge[0] + 1} {edge[1] + 1}\n")  # Add "edge" and 1 to each endpoint

        print(f"Edge list written to {output_file}")
    except Exception as e:
        print(f"An error occurred while writing the edge list to {output_file}: {e}")

