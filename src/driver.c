#include <stdio.h>
#include "graph.h"
#include "matching.h"

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
   
   M = MaximumCardinalityMatching(G);
   fprintf(stdout, "The %d edges of a maximum-cardinality matching are\n",
           ListSize(M));
   N = 1;
   ForAllGraphVertices(V, G, P)
      VertexRelabel(V, (VertexData) N++);
   ForAllEdges(E, M, P)
      fprintf(stdout, "(%d, %d)\n",
         (int) VertexLabel(EdgeFrom(E)), (int) VertexLabel(EdgeTo(E)));
   DestroyList(M);
   
   DestroyGraph(G);
}
