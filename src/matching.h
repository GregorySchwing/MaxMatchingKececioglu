/*
 * matching.h -- Maximum cardinality matching definitions
 */

/*
 * Copyright 1996 by John Kececioglu
 */


#ifndef MatchingInclude
#define MatchingInclude
 

#include "list.h"
#include "graph.h"


extern List *MaximumCardinalityMatching Proto(( Graph *G ));
extern List *MaximalMatching            Proto(( Graph *G ));


#endif /* MatchingInclude */
