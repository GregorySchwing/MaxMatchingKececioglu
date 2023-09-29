import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

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

# Calculate relative speedup using the mean seconds for each NUMSTACK_GPU value
relative_speedup_df = combined_df.groupby(['C', 'V', 'NUMSTACK_GPU'])[['seconds_CPU', 'seconds_GPU']].mean().reset_index()
relative_speedup_df['relative_speedup'] = relative_speedup_df['seconds_CPU'] / relative_speedup_df['seconds_GPU']

# Get unique C values from the combined dataframe
unique_c_values = relative_speedup_df['C'].unique()

# Determine the number of subplots needed
num_subplots = len(unique_c_values)

# Calculate the number of rows and columns for the subplot grid
num_rows = int(num_subplots ** 0.5)
num_cols = (num_subplots + num_rows - 1) // num_rows

# Define a list of marker symbols
marker_symbols = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'H']

# Use the colorblind-accessible palette from seaborn
colors = sns.color_palette("colorblind", num_subplots)

# Create a figure with subplots arranged in a grid
fig, axs = plt.subplots(num_rows, num_cols, figsize=(20, 13))
fig.suptitle('Relative Speedup versus Vertices for Different Numbers (B) of Blocks', fontsize=16, y=1.0)
fig.text(0.5, 0.95, 'C=M/N', fontsize=16, ha='center')  # Add the subtitle

# Flatten the axs array if it's multidimensional
axs = axs.ravel()

# Create patches at the top of the figure with NUMSTACKS as text labels for the first unique C value
first_c_value = unique_c_values[0]
patches = []
color_mapping = {}
for i, numstack in enumerate(relative_speedup_df[relative_speedup_df['C'] == first_c_value]['NUMSTACK_GPU'].unique()):
    color = colors[i % len(colors)]  # Cycle through colors
    color_mapping[numstack] = color
    patches.append(mpatches.Patch(color=color, label=f'B={int(numstack)}'))

# Add the patches to the top of the figure
fig.legend(handles=patches, loc='upper center', ncol=len(patches), bbox_to_anchor=(0.5, 0.95))

for i, c_value in enumerate(unique_c_values):
    ax = axs[i]
    df_c = relative_speedup_df[relative_speedup_df['C'] == c_value]

    ax.set_title(f'C={c_value}')
    ax.set_xlabel('V')
    ax.set_ylabel('Relative Speedup')

    # Plot relative speedup for each NUMSTACK_GPU value with different marker symbols and colors
    legend_handles = []
    for j, numstack in enumerate(df_c['NUMSTACK_GPU'].unique()):
        df_numstack = df_c[df_c['NUMSTACK_GPU'] == numstack]
        label = f'N={int(numstack)}'
        marker_symbol = marker_symbols[j % len(marker_symbols)]  # Cycle through marker symbols
        color = color_mapping[numstack]  # Use color from the mapping
        line = ax.plot(df_numstack['V'], df_numstack['relative_speedup'], marker=marker_symbol, linestyle='-', markersize=6, label=label, color=color)

        # Calculate and plot the standard deviation as a shaded area
        std_dev = df_numstack[['seconds_CPU', 'seconds_GPU']].std(axis=1)
        ax.fill_between(df_numstack['V'], df_numstack['relative_speedup'] - std_dev, df_numstack['relative_speedup'] + std_dev, alpha=0.2, color=color)
        
        legend_handles.append(Line2D([0], [0], color=color, marker=marker_symbol, markersize=6, label=label))

# Create a single horizontal legend outside the subplots
fig.legend(handles=legend_handles, loc='upper center', ncol=len(df_c['NUMSTACK_GPU'].unique()), bbox_to_anchor=(0.5, -0.05))
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('relative_speedup_plot.png')
# Adjust spacing between subplots
# Show the plot
plt.show()

