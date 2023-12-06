#include <stdio.h>
#include "graph.h"
#include "matching.h"
#include <time.h>
#include <unistd.h>
#include <string.h>

#include "../matchmaker2/main_lib.cuh"
#include "../BFSHonestPaths/bipartite.h"
#include "../ms-bfs-graft/msBFSGraft_lib.h"

#include <sys/time.h>
double getTimeOfDay() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec / 1000000.0;
}

typedef ListCell Cell;

Void main (int argc, char **argv)
{
   int   N,EdgeListSize;
   List *M;
   Cell *P;
   

   Graph  *G;
   Vertex *V;
   Edge   *E;
   FILE *log;
   log = fopen("log.txt", "w");
   int nr, nc, nn;
   int * rows;
   int * cols;
   int * matching;
   double start_time_wall, end_time_wall;
   clock_t start_time_e2e = clock();
   start_time_wall = getTimeOfDay();
   /*
   int match_type = main_lib(argc, argv, log, &rows, &cols, &matching, &nr, &nc, &nn);
   if (match_type > 11){
      BFSHonestWrapper(rows, cols, matching, nr, nn, 1);
   }
   */
   int match_type = main_lib_msbfsgraft(argc, argv, &rows, &cols, &matching, &nr, &nc, &nn);
   match_type = 11;
   N = nr;
   EdgeListSize = nn/2;
   G = CreateGraphFromCSC_MS_BFS_GRAFT(rows, cols, matching, nr, nc, nn, match_type);

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
   strcpy(outputFilename, "Results.csv");
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
      fprintf(output_file, "%s,%s,%s,%s,%s,%s\n", "Filename", "V","E","M", "milliseconds","seconds");
   }
   if (argc>1){
      strcpy(inputFilename, argv[1]);
      fprintf(output_file, "%s,%d,%d,%d,%f,%f\n", inputFilename, N,EdgeListSize,ListSize(M),elapsed_time_ms,elapsed_time_ms/1000.0);
   } else {
      fprintf(output_file, "%s,%d,%d,%d,%f,%f\n", "UNKNOWN", N,EdgeListSize,ListSize(M),elapsed_time_ms,elapsed_time_ms/1000.0);
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
