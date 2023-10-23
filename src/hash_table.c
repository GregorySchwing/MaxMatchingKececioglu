#include <stdio.h>
#include <stdlib.h>
#include "hash_table.h"

#define TABLE_SIZE 100

struct HashTable {
    int size;
    KeyValuePair **table;
};

int hashFunction(OrderedPair key, int tableSize) {
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
    newPair->next = NULL;

    if (table->table[index] == NULL) {
        table->table[index] = newPair;
    } else {
        KeyValuePair *current = table->table[index];
        while (current->next != NULL) {
            current = (KeyValuePair *)current->next; // Type cast here.
        }
        current->next = newPair;
    }
}

Edge *get(HashTable *table, OrderedPair key) {
    int index = hashFunction(key, table->size);
    KeyValuePair *pair = table->table[index];
    
    while (pair != NULL) {
        if (pair->key.x == key.x && pair->key.y == key.y) {
            return pair->value;
        }
        pair = (KeyValuePair *)pair->next; // Type cast here.
    }

    return NULL;
}

void removeKey(HashTable *table, OrderedPair key) {
    int index = hashFunction(key, table->size);
    KeyValuePair *current = table->table[index];
    KeyValuePair *prev = NULL;

    while (current != NULL) {
        if (current->key.x == key.x && current->key.y == key.y) {
            if (prev != NULL) {
                prev->next = current->next;
            } else {
                table->table[index] = (struct KeyValuePair *)current->next; // Add a type cast here.
            }
            free(current);
            return; // Key removed successfully.
        }
        prev = current;
        current = (KeyValuePair *)current->next; // Type cast here.
    }
}

void destroyHashTable(HashTable *table) {
    for (int i = 0; i < table->size; i++) {
        KeyValuePair *current = table->table[i];
        while (current != NULL) {
            KeyValuePair *next = (KeyValuePair *)current->next; // Type cast here.
            free(current);
            current = next;
        }
    }
    free(table->table);
    free(table);
}
