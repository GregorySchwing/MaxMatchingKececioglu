#include <stdio.h>
#include "graph.h"
#include "matching.h"
#include <time.h>
#include <unistd.h>
#include <string.h>
#include <libgen.h>
#include "../matchmaker2/main_lib.cuh"
#include "../BFSHonestPaths/bipartite.h"
#include "../ms-bfs-graft/msBFSGraft_lib.h"

#include <sys/time.h>
double getTimeOfDay() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec / 1000000.0;
}

// Helper method to print usage instructions and call the appropriate code
void executeCode(int config_arg, int config_arg2, int argc, char *argv[], int **rows, int **cols, int **matching, int *nr_ptr, int *nc_ptr, int *nn_ptr) {
    switch (config_arg) {
        case 0:
            printf("Wrapper Configuration: MS-BFS_GRAFT\n");
            // Call MS-BFS_GRAFT with the rest of the arguments and pointers
            // ...
            int parallelKS = 1;
            int match_type = main_lib_msbfsgraft(argc, argv, rows, cols, matching, nr_ptr, nc_ptr, nn_ptr, config_arg2);
            break;
        case 1:
            printf("Wrapper Configuration: Matchmaker2\n");
            // Call Matchmaker2 with the rest of the arguments and pointers
            FILE *log;
            int match_type2 = main_lib(argc, argv, log, rows, cols, matching, nr_ptr, nc_ptr, nn_ptr, config_arg2);
            break;
        case 2:
            printf("Wrapper Configuration: BFSHonestPath -UNSUPPORTED\n");
            exit(0);
            // Call BFSHonestPath with the rest of the arguments and pointers
            BFSHonestWrapper(*rows, *cols, *matching, *nr_ptr, *nn_ptr, 1);

            break;
        default:
            printf("Invalid configuration argument. Use 0, 1, or 2.\n");
    }
}

// Enumeration of algorithm names
enum Algorithm {
    MS_BFS_GRAFT = 0,
    MATCHMAKER_2 = 1,
    BFS_HONEST_PATH = 2,
    NUM_ALGORITHMS // Number of algorithms, automatically set to 3
};

// Array of corresponding algorithm names
const char *algorithmNames[] = {
    "MS-BFS_GRAFT",
    "Matchmaker2",
    "BFSHonestPath"
};


// Enumeration for boolean values
enum Boolean {
    TRUE = 0,
    FALSE = 1
};

// Array of corresponding boolean strings
const char *booleanStrings[] = {
    "INITIALIZE",
    "JUST_READ_FILE",
};

typedef ListCell Cell;

Void main (int argc, char **argv)
{

   // Check if there are enough arguments
   if (argc < 3) {
      printf("Usage: %s <config_arg1> <config_arg2> [code_args...]\n", argv[0]);
      printf("   - config_arg1: 0 for MS-BFS_GRAFT\n");
      printf("                  1 for Matchmaker2\n");
      printf("                  2 for BFSHonestPath\n");
      printf("   - config_arg2: 0 : INITIALIZE\n");
      printf("                  1 : JUST_READ_FILE\n");
      return;
   }

   // Extract the configuration argument
   int config_arg = atoi(argv[1]);
   int config_arg2 = atoi(argv[2]);

   int   N,EdgeListSize;
   List *M;
   Cell *P;
   

   Graph  *G;
   Vertex *V;
   Edge   *E;
   int nr, nc, nn;
   int * rows;
   int * cols;
   int * matching;
   double start_time_wall, end_time_wall;
   double start_time_init, end_time_init;
   clock_t start_time_e2e = clock();
   start_time_wall = getTimeOfDay();
   /*
   
   if (match_type > 11){
   }
   */
   // Call the helper method to execute the appropriate code
   start_time_init = getTimeOfDay();
   executeCode(config_arg, config_arg2, argc - 2, argv + 2, &rows, &cols, &matching, &nr, &nc, &nn);
   end_time_init = getTimeOfDay();
   N = nr;
   EdgeListSize = nn/2;
   if (config_arg < 1){
      G = CreateGraphFromCSC_MS_BFS_GRAFT(rows, cols, matching, nr, nc, nn, config_arg2);
   } else {
      G = CreateGraphFromCSC(rows, cols, matching, nr, nc, nn, config_arg2);
   }
   FILE *f;

   clock_t start_time, end_time;
   double elapsed_time_ms;
   double total_time_ms;
   #ifndef NDEBUG
   const char* extensionX = ".augP";
   char outputFilenameX[500];
   strcpy(outputFilenameX, argv[1]);
   strcat(outputFilenameX, extensionX);
   const char* extensionY = ".augT";
   char outputFilenameY[500];
   strcpy(outputFilenameY, argv[1]);
   strcat(outputFilenameY, extensionY);
   const char* extensionZ = ".dead";
   char outputFilenameZ[500];
   strcpy(outputFilenameZ, argv[1]);
   strcat(outputFilenameZ, extensionZ);
   FILE *output_fileX;
   FILE *output_fileY;
   FILE *output_fileZ;
   output_fileX = fopen(outputFilenameX, "w");
   output_fileY = fopen(outputFilenameY, "w");
   output_fileZ = fopen(outputFilenameZ, "w");
   #endif

   #ifndef NDEBUG
   M = MaximumCardinalityMatchingTrack(G,output_fileX,output_fileY,output_fileZ);
   fclose(output_fileX);
   fclose(output_fileY);
   fclose(output_fileZ);
   #endif
   // Record the starting time
   start_time = clock();
   M = MaximumCardinalityMatching(G);
   end_time = clock();
   end_time_wall = getTimeOfDay();

   // Calculate the elapsed time in milliseconds
   elapsed_time_ms = ((double)(end_time - start_time) / CLOCKS_PER_SEC) * 1000.0;
   total_time_ms = ((double)(end_time - start_time_e2e) / CLOCKS_PER_SEC) * 1000.0;
   // Print the elapsed time in milliseconds
   printf("Total CPU Time: %.2f milliseconds\n", total_time_ms);
   printf("Total CPU Time: %.2f seconds\n", total_time_ms/1000.0);
   // Calculate and print the elapsed time
   printf("Total Wall time: %f seconds\n", end_time_wall - start_time_wall);
   printf("Elapsed Time: %.2f milliseconds\n", elapsed_time_ms);
   printf("Elapsed Time: %.2f seconds\n", elapsed_time_ms/1000.0);
   fprintf(stdout, "There are %d edges in the maximum-cardinality matching.\n",
           ListSize(M));

   char inputFilename[500];
   char outputFilename[500];
   strcpy(outputFilename, "WrapperResults.csv");
   FILE *output_file;
   if (access(outputFilename, F_OK) == 0)
   {
      // file exists
      output_file = fopen(outputFilename, "a");
   }
   else
   {
      // file doesn't exist
      output_file = fopen(outputFilename, "w");
      fprintf(output_file, "%s,%s,%s,%s,%s,%s,%s,%s,%s\n", "INITALGO", "PREPROCESSING", "Filename", "V","E","M", "INIT_TIME(S)","SS_DFS_TIME(s)","TOTAL_WALL_CLOCK(s)");
   }
   if (argc>1){
      strcpy(inputFilename,  basename(argv[3]));
      fprintf(output_file, "%s,%s,%s,%d,%d,%d,%f,%f,%f\n", algorithmNames[config_arg], booleanStrings[config_arg2], inputFilename, N,EdgeListSize,ListSize(M),elapsed_time_ms/1000.0,end_time_init-start_time_init,end_time_wall - start_time_wall);
   } else {
      fprintf(output_file, "%s,%d,%d,%d,%f,%f\n", "UNKNOWN", N,EdgeListSize,ListSize(M),elapsed_time_ms/1000.0,end_time_wall - start_time_wall);
   }
   fclose(output_file);

   /*
   N = 1;
   ForAllGraphVertices(V, G, P)
      VertexRelabel(V, (VertexData) N++);
   ForAllEdges(E, M, P)
      fprintf(stdout, "(%d, %d)\n",
         (int) VertexLabel(EdgeFrom(E)), (int) VertexLabel(EdgeTo(E)));
   */
   DestroyList(M);
   
   DestroyGraph(G);

}
