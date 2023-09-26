#include <stdio.h>
#include "graph.h"
#include "matching.h"
#include <time.h>
#include <unistd.h>

typedef ListCell Cell;

Void main ()
{
   int   N;
   List *M;
   Cell *P;
   
   Graph  *G;
   Vertex *V;
   Edge   *E;
  
   
   G = ReadGraph(stdin);
   clock_t start_time, end_time;
   double elapsed_time_ms;

   // Record the starting time
   start_time = clock();
   M = MaximumCardinalityMatching(G);
   end_time = clock();

   // Calculate the elapsed time in milliseconds
   elapsed_time_ms = ((double)(end_time - start_time) / CLOCKS_PER_SEC) * 1000.0;

   // Print the elapsed time in milliseconds
   printf("Elapsed Time: %.2f milliseconds\n", elapsed_time_ms);
   printf("Elapsed Time: %.2f seconds\n", elapsed_time_ms/1000.0);
   fprintf(stdout, "The %d edges of a maximum-cardinality matching are\n",
           ListSize(M));

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
      fprintf(output_file, "%s,%s,%s,%s,%s,%s\n", "Filename", "V","E","M", "milliseconds" "seconds");
   }
   fprintf(output_file, "%s,%d,%d,%d,%f,%f\n", "test", N,N,ListSize(M),elapsed_time_ms,elapsed_time_ms/1000.0);
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
