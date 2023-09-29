import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file for GPUResults (change the path as needed)
df_gpu = pd.read_csv('GPUResults.csv')

# Read the CSV file for CPUResults (change the path as needed)
df_cpu = pd.read_csv('CPUResults.csv')

# Rename columns in the GPU dataframe by removing the 'GPU_' prefix
df_gpu.columns = df_gpu.columns.str.replace('GPU_', '')

# Rename columns in the CPU dataframe by removing the 'CPU_' prefix
df_cpu.columns = df_cpu.columns.str.replace('CPU_', '')

# Add a 'Device' column and set it to 'GPU' for GPUResults
df_gpu['Device'] = 'GPU'

# Add a 'Device' column and set it to 'CPU' for CPUResults
df_cpu['Device'] = 'CPU'

# Extract the wildcards V, E, and C from the Filename for GPUResults
df_gpu[['V', 'E', 'C']] = df_gpu['Filename'].str.extract(r'(\d+)_(\d+)_(\d+)_RMAT\.txt\.mtx')

# Convert 'C' column to integer type for GPUResults
df_gpu['C'] = df_gpu['C'].astype(int)

# Extract the wildcards V, E, and C from the Filename for CPUResults
df_cpu[['V', 'E', 'C']] = df_cpu['Filename'].str.extract(r'(\d+)_(\d+)_(\d+)_RMAT\.txt\.mtx')

# Convert 'C' column to integer type for CPUResults
df_cpu['C'] = df_cpu['C'].astype(int)

# Add a 'NUMSTACK' column with each row set to 1 for CPUResults
df_cpu['NUMSTACK'] = 1

# Merge GPU and CPU dataframes on 'C' and 'V'
combined_df = df_gpu.merge(df_cpu, on=['C', 'V'], suffixes=('_GPU', '_CPU'), how='outer')

# Calculate relative speedup by dividing CPU seconds by GPU seconds
combined_df['relative_speedup'] = combined_df['seconds_CPU'] / combined_df['seconds_GPU']

# Get unique C values from the combined dataframe
unique_c_values = combined_df['C'].unique()

# Check if there are unique C values before creating subplots
if len(unique_c_values) > 0:
    # Create a figure with subplots arranged in a grid
    fig, axs = plt.subplots(len(unique_c_values), 1, figsize=(10, 6 * len(unique_c_values)), sharex=True)
    fig.suptitle('Relative Speedup vs. V (Grouped by C and NUMSTACK)', fontsize=16)

    # Iterate through unique C values and create subplots in the grid
    for i, c_value in enumerate(unique_c_values):
        ax = axs[i]
        df_c = combined_df[combined_df['C'] == c_value]

        ax.set_title(f'C={c_value}')
        ax.set_xlabel('V')
        ax.set_ylabel('Relative Speedup')

        # Plot relative speedup for each NUMSTACK value
        for numstack in df_c['NUMSTACK_GPU'].unique():
            df_numstack = df_c[df_c['NUMSTACK_GPU'] == numstack]
            label = f'NUMSTACK={numstack}'
            ax.plot(df_numstack['V'], df_numstack['relative_speedup'], marker='o', linestyle='-', markersize=6, label=label)

        ax.legend(title='NUMSTACK')

    # Adjust spacing between subplots
    plt.tight_layout(rect=[0, 0, 1, 0.97])

    # Show the plot
    plt.show()
else:
    print("No unique C values found in the combined dataframe.")

