#include <stdio.h>
#include "graph.h"
#include "matching.h"
#include <time.h>
#include <unistd.h>
#include <string.h>

#include "../matchmaker2/main_lib.cuh"

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
   main_lib(argc, argv, log, &rows, &cols, &matching, &nr, &nc, &nn);
   N = nr;
   EdgeListSize = nn/2;
   G = CreateGraphFromCSC(rows, cols, matching, nr, nc, nn);

   FILE *f;

   clock_t start_time, end_time;
   double elapsed_time_ms;
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

   // Calculate the elapsed time in milliseconds
   elapsed_time_ms = ((double)(end_time - start_time) / CLOCKS_PER_SEC) * 1000.0;

   // Print the elapsed time in milliseconds
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
