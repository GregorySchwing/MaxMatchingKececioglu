#include <stdio.h>
#include <stdlib.h>
#include "hash_table.h"

#define TABLE_SIZE 100 // You can adjust the table size as needed.

struct HashTable {
    int size;
    KeyValuePair **table;
};

int hashFunction(OrderedPair key, int tableSize) {
    // A simple hash function for OrderedPair keys.
    return (key.x + key.y) % tableSize;
}

HashTable *createHashTable(int size) {
    HashTable *table = (HashTable *)malloc(sizeof(HashTable));
    if (table == NULL) {
        perror("Unable to allocate memory for the hash table.");
        exit(1);
    }

    table->size = size;
    table->table = (KeyValuePair **)malloc(size * sizeof(KeyValuePair *));
    if (table->table == NULL) {
        perror("Unable to allocate memory for the hash table array.");
        free(table);
        exit(1);
    }

    for (int i = 0; i < size; i++) {
        table->table[i] = NULL;
    }

    return table;
}

void insert(HashTable *table, OrderedPair key, Edge *value) {
    int index = hashFunction(key, table->size);
    KeyValuePair *newPair = (KeyValuePair *)malloc(sizeof(KeyValuePair));
    if (newPair == NULL) {
        perror("Unable to allocate memory for a new key-value pair.");
        exit(1);
    }

    newPair->key = key;
    newPair->value = value;
    table->table[index] = newPair;
}

Edge *get(HashTable *table, OrderedPair key) {
    int index = hashFunction(key, table->size);
    KeyValuePair *pair = table->table[index];
    if (pair != NULL && pair->key.x == key.x && pair->key.y == key.y) {
        return pair->value;
    }
    return NULL; // Key not found.
}

void removeKey(HashTable *table, OrderedPair key) {
    int index = hashFunction(key, table->size);
    KeyValuePair *pair = table->table[index];
    if (pair != NULL && pair->key.x == key.x && pair->key.y == key.y) {
        free(pair); // Free the memory of the key-value pair.
        table->table[index] = NULL;
    }
}

void destroyHashTable(HashTable *table) {
    for (int i = 0; i < table->size; i++) {
        KeyValuePair *pair = table->table[i];
        if (pair != NULL) {
            free(pair);
        }
    }
    free(table->table);
    free(table);
}
