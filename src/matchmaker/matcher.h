
/*
 * matcher.h -- C-API for matchmaker2
 */

/*
 * Copyright 2023 by Greg Schwing
 */


#ifndef MATCHER
#define MATCHER


// *.h file
#include "../graph.h"

// ...
#ifdef __cplusplus
#define EXTERNC extern "C"
#else
#define EXTERNC
#endif

EXTERNC void allocateGPUMatcher(Graph * graph);

#undef EXTERNC
// ...


#endif
