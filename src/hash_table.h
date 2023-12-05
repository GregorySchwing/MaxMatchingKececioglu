#ifndef HASH_TABLE_H
#define HASH_TABLE_H

#include "edge_vertex.h"


typedef struct {
    int x;
    int y;
} OrderedPair;

typedef struct KeyValuePair {
    OrderedPair key;
    Edge *value;
    struct KeyValuePair* next; // Linked list for separate chaining.
} KeyValuePair;

typedef struct HashTable HashTable;

HashTable *createHashTable(int size);
void insert(HashTable *table, OrderedPair key, Edge *value);
Edge *get(HashTable *table, OrderedPair key);
void removeKey(HashTable *table, OrderedPair key);
void destroyHashTable(HashTable *table);

#endif
