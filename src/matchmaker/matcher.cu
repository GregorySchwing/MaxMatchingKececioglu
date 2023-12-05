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
#include "matcher.h"
#include "../graph.h"
/*
#include "GreedyMatcher.cuh"
#include "bfs.cuh"
*/
#include <chrono>

void allocateGPUMatcher(Graph * G){
    std::chrono::time_point<std::chrono::steady_clock> m_StartTime = std::chrono::steady_clock::now();
    int n = G->EL.N;
    int m = G->EL.M;
    Matcher mm;
    mm._bfs = &n;
    G->mm = mm;

    //BFS b(csr, gm);
}