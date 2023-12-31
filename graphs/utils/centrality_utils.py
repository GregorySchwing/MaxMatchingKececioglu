import os
import random
import numpy as np
import pandas as pd
import cudf  # Import cuDF
import networkx as nx
import matplotlib.pyplot as plt

try:
    import cugraph
    cugraph_available = True
except ImportError:
    cugraph_available = False

def calculate_centrality_and_triangles(G, num_vertices, num_edges, output_file):
    if cugraph_available:
        import cugraph

        # Calculate degree centrality using cuGraph
        degree_centrality = cugraph.centrality.degree_centrality(G)

        # Calculate betweenness centrality using cuGraph
        betweenness_centrality = cugraph.centrality.betweenness_centrality(G)

        # Calculate eigenvector centrality using cuGraph
        eigenvector_centrality = cugraph.centrality.eigenvector_centrality(G)

        # Calculate Katz centrality using cuGraph
        katz_centrality = cugraph.centrality.katz_centrality(G)


        # Calculate clustering coefficient using NetworkX
        #clustering_coefficient = 0
        edge_list_df = G.view_edge_list().to_pandas()
        Gnx=nx.from_pandas_edgelist(edge_list_df, source='src', target='dst')
        # Calculate clustering coefficient using NetworkX
        clustering_coefficient_dict = nx.clustering(Gnx)
        clustering_coefficient_df_host = pd.DataFrame(list(clustering_coefficient_dict.items()), columns=['Node', 'Clustering_Coefficient'])
        clustering_coefficient_df=cudf.from_pandas(clustering_coefficient_df_host)

        # Calculate the number of triangles
        triangles = cugraph.triangle_count(G)
        # Append to log file
        append_to_log_file(num_vertices, num_edges, output_file, clustering_coefficient_df['Clustering_Coefficient'].mean(),
                        degree_centrality['degree_centrality'].mean(), betweenness_centrality['betweenness_centrality'].mean(),
                        eigenvector_centrality['eigenvector_centrality'].mean(), katz_centrality['katz_centrality'].mean(), triangles['counts'].mean())

        # Save histogram data using cuDF
        save_histogram_data(triangles['counts'], "TriangleCounts", output_file)
        save_histogram_data(clustering_coefficient_df['Clustering_Coefficient'], "ClusteringCoefficient", output_file)
        save_histogram_data(degree_centrality['degree_centrality'], "DegreeCentrality", output_file)
        save_histogram_data(betweenness_centrality['betweenness_centrality'], "BetweennessCentrality", output_file)
        save_histogram_data(eigenvector_centrality['eigenvector_centrality'], "EigenvectorCentrality", output_file)
        save_histogram_data(katz_centrality['katz_centrality'], "KatzCentrality", output_file)
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

        # Save histogram data using Pandas
        save_histogram_data(list(degree_centrality.values()), "DegreeCentrality", output_file)
        save_histogram_data(list(betweenness_centrality.values()), "BetweennessCentrality", output_file)
        save_histogram_data(list(eigenvector_centrality.values()), "EigenvectorCentrality", output_file)
        save_histogram_data(list(katz_centrality.values()), "KatzCentrality", output_file)

def append_to_log_file(num_vertices, num_edges, output_file, clustering_coefficient,
                       degree_centrality, betweenness_centrality,
                       eigenvector_centrality, katz_centrality, triangles):
    # Extract the base filename without extension
    base_filename = os.path.basename(output_file)

    # Create or append to the log CSV file
    log_columns = ["Vertices", "Edges", "BaseFilename", "ClusteringCoefficient", "AverageDegreeCentrality",
                   "AverageBetweennessCentrality", "AverageEigenvectorCentrality",
                   "AverageKatzCentrality", "Triangles"]

    if os.path.isfile("log.csv"):
        log_df = pd.read_csv("log.csv")
    else:
        log_df = pd.DataFrame(columns=log_columns)

    log_df = log_df.append({
        "Vertices": num_vertices,
        "Edges": num_edges,
        "BaseFilename": f"{base_filename}",
        "ClusteringCoefficient": clustering_coefficient,
        "AverageDegreeCentrality": degree_centrality,
        "AverageBetweennessCentrality": betweenness_centrality,
        "AverageEigenvectorCentrality": eigenvector_centrality,
        "AverageKatzCentrality": katz_centrality,
        "Triangles": triangles
    }, ignore_index=True)

    log_df.to_csv("log.csv", index=False)

def save_histogram_data(centrality_values, centrality_name, output_file):
    histogram_data, bin_edges = np.histogram(centrality_values, bins=20)
    
    # Convert to cuDF DataFrame
    histogram_df = cudf.DataFrame({
        "BinEdges": bin_edges[:-1],
        "Frequency": histogram_data
    })
    
    # Save the cuDF DataFrame to CSV
    histogram_df.to_pandas().to_csv(f"{output_file}_{centrality_name}_histogram.csv", index=False)

def write_edge_list(G, output_file, num_vertices):
    try:
        # Extract the edge list as a cuDF DataFrame
        edge_list = G.view_edge_list()
        # Add 1 to each endpoint to match the desired format
        edge_list['src'] += 1
        edge_list['dst'] += 1
        # Set the index to a constant string
        constant_index = 'edge'
        edge_list.index = [constant_index] * len(edge_list)
        # Write the number of vertices and edges
        with open(output_file, 'w') as f:
            f.write(f"vertices {num_vertices}\n")
            f.write(f"edges {len(edge_list)}\n")

        # Append the edge list to the file using cuDF
        with open(output_file, 'a') as f:
            edge_list.to_pandas().to_csv(f, sep=' ', header=False, index_label='edge')

        print(f"Edge list written to {output_file}")
    except Exception as e:
        print(f"An error occurred while writing the edge list to {output_file}: {e}")