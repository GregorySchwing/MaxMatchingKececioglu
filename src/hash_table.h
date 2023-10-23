#ifndef HASH_TABLE_H
#define HASH_TABLE_H

#include "edge_vertex.h"

// Forward declaration of the Edge structure as an incomplete type.

typedef struct {
    int x;
    int y;
} OrderedPair;

typedef struct {
    OrderedPair key;
    Edge *value; // Use the forward declaration.
} KeyValuePair;

typedef struct HashTable HashTable;

HashTable *createHashTable(int size);
void insert(HashTable *table, OrderedPair key, Edge *value);
Edge *get(HashTable *table, OrderedPair key);
void removeKey(HashTable *table, OrderedPair key);
void destroyHashTable(HashTable *table);

#endif
