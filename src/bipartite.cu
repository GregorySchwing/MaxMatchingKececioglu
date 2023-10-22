/*
 * bipartite.c -- Initialize bipartite graph on GPU
 */

/*
 * Copyright 2023 by Greg Schwing
 */


/*
 * Synopsis
 *
 * This implementation of bipartite matching on the GPU can accelerate general
 * graph matching by initializing nearly the entire matching in parallel.
 *
 */

/*
 * Author
 *
 * Greg Schwing
 * gregory.schwing@med.wayne.edu
 *
 * Department of Computer Science
 * Wayne State University
 * Detroit, MI 48201
 *
 */

/*
 * History
 *
 * 22 October 2023
 * First draft.
 *
 */
#include "bipartite.h"
#include "CSRGraph.cuh"
#include "graph.h"
#include "list.h"

typedef ListCell Cell;

void bipartite(Graph * G){
    register Cell   *P;
    register Vertex *V;
    register Edge   *E;
    ForAllGraphVertices(V, G, P)
    {
    }
    ForAllGraphEdges(E, G, P)
    {
    }
}