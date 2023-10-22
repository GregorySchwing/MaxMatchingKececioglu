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
#include "set.h"

/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 *
 * Types
 *
 */


typedef ListCell Cell;

typedef struct
{
   Vertex *BaseField;
}
SetAttribute;

typedef struct
{
   Element *BlossomField;
   Edge    *MatchField;
   Edge    *TreeField;
   Edge    *BridgeField;
   Vertex  *ShoreField;
   short    LabelField;
   int      AgeField;
   Cell    *SelfField;
   VertexData    OriginalVertexLabelField;
   SetAttribute *OriginalSetLabelField;

   
#ifdef Debug
   
   int   NameField;
   List *MembersField;
   List *ChildrenField;
   
#endif /* Debug */
   
   
}
VertexAttribute;

#if Debug
extern List *MaximumCardinalityMatchingTrack Proto((Graph *G, FILE * outputFileX,FILE * outputFileY,FILE * outputFileZ));
#endif
extern List *MaximumCardinalityMatching Proto(( Graph *G ));
extern List *MaximalMatching            Proto(( Graph *G ));


#endif /* MatchingInclude */
