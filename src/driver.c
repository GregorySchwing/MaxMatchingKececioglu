#include <stdio.h>
#include "graph.h"
#include "matching.h"
#include <time.h>
#include <unistd.h>
#include <string.h>
#include <libgen.h>

#include <sys/time.h>
double getTimeOfDay() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec / 1000000.0;
}

typedef ListCell Cell;
int main(int argc, char **argv){}
void match (int * rows, int * cols,  int * matching, int nr, int nc, int nn)
{

   int   N,EdgeListSize;
   List *M;
   Cell *P;
   

   Graph  *G;
   Vertex *V;
   Edge   *E;
   //int nr, nc, nn;
   //int * rows;
   //int * cols;
   //int * matching;
   double start_time_wall, end_time_wall;
   double start_time_csc_2_g, end_time_csc_2_g;
   double start_time_match, end_time_match;
   start_time_wall = getTimeOfDay();
   N = nr;
   EdgeListSize = nn/2;
   start_time_csc_2_g = getTimeOfDay();
   G = CreateGraphFromCSC(rows, cols, matching, nr, nc, nn, 1);
   end_time_csc_2_g = getTimeOfDay();
   printf("CSC to Graph conversion time: %f seconds\n", end_time_csc_2_g - start_time_csc_2_g);
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
   start_time_match = getTimeOfDay();
   M = MaximumCardinalityMatching(G);
   end_time_match = getTimeOfDay();
   end_time_wall = getTimeOfDay();

   printf("Match time: %f seconds\n", end_time_match - start_time_match);


   // Calculate and print the elapsed time
   printf("Total Wall time: %f seconds\n", end_time_wall - start_time_wall);
   fprintf(stdout, "There are %d edges in the maximum-cardinality matching.\n",
           ListSize(M));

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
