
/*
 * biparite.h -- Initialize bipartite graph
 */

/*
 * Copyright 2023 by Greg Schwing
 */


#ifndef Bipartite
#define Bipartite

// *.h file
#include "graph.h"

// ...
#ifdef __cplusplus
#define EXTERNC extern "C"
#else
#define EXTERNC
#endif

EXTERNC void bipartite(Graph * graph);

#undef EXTERNC
// ...

#endif