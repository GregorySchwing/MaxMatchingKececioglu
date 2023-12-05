#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s input_matrix_market.txt output.txt\n", argv[0]);
        return 1;
    }

    clock_t start_time, end_time;
    double elapsed_time_ms;

    // Record the starting time
    start_time = clock();

    const char *input_file_name = argv[1];
    const char *output_file_name = argv[2];

    FILE *input_file = fopen(input_file_name, "r");
    if (input_file == NULL) {
        perror("Error opening input file");
        return 1;
    }

    int num_rows = 0, num_edges = 0;
    int i, j;

    // Skip lines starting with '%'
    char line[256];
    while (fgets(line, sizeof(line), input_file) != NULL) {
        if (line[0] != '%') {
            break; // Found the header line
        }
    }

    // Parse the header line with 3 tokens
    if (sscanf(line, "%d %*d %d", &num_rows, &num_edges) != 2) {
        fprintf(stderr, "Invalid header format\n");
        fclose(input_file);
        return 1;
    }

    // Preallocate memory for the edges
    int (*edges)[2] = (int(*)[2])malloc(num_edges * sizeof(int[2]));
    if (edges == NULL) {
        perror("Memory allocation error");
        fclose(input_file);
        return 1;
    }

    // Read and populate the edges
    for (int k = 0; k < num_edges; k++) {
        if (fscanf(input_file, "%d %d", &i, &j) != 2) {
            fprintf(stderr, "Invalid edge format at line %d\n", k + 2);
            fclose(input_file);
            free(edges);
            return 1;
        }
        edges[k][0] = i;
        edges[k][1] = j;
    }

    fclose(input_file);

    // Record the ending time
    end_time = clock();

    // Calculate the elapsed time in milliseconds
    elapsed_time_ms = ((double)(end_time - start_time) / CLOCKS_PER_SEC) * 1000.0;

    // Print the elapsed time in milliseconds
    printf("Elapsed Time: %.2f milliseconds\n", elapsed_time_ms);

    // Write the edge list to the output file
    FILE *output_file = fopen(output_file_name, "w");
    if (output_file == NULL) {
        perror("Error opening output file");
        free(edges);
        return 1;
    }

    fprintf(output_file, "vertices %d\n", num_rows);
    fprintf(output_file, "edges %d\n", num_edges);

    for (int k = 0; k < num_edges; k++) {
        fprintf(output_file, "edge %d %d\n", edges[k][0], edges[k][1]);
    }

    fclose(output_file);
    free(edges);

    return 0;
}
