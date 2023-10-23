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
#include "GreedyMatcher.cuh"
#include <chrono>

void bipartite(Graph * G){
    int n = G->EL.N;
    int m = G->EL.M;
    //printf("Generating CSR with %d rows, %d columns\n",m,m);
    CSRGraph csr(n,m,G->EL.Rows,G->EL.Cols,G->EL.Matching);
    
    GreedyMatcher gm(csr);
    std::chrono::time_point<std::chrono::steady_clock> m_StartTime = std::chrono::steady_clock::now();
    int numAugmented = gm.maxMatch();
    std::chrono::time_point<std::chrono::steady_clock> m_EndTime = std::chrono::steady_clock::now();
    double elapsedSeconds = std::chrono::duration_cast<std::chrono::milliseconds>(m_EndTime - m_StartTime).count() / 1000.0;  
    std::cout << "Greedy match seconds: " << elapsedSeconds << "; edges augmented: " << numAugmented << std::endl;
    csr.copyMatchingBack();
    //BFS b(csr, gm);
}