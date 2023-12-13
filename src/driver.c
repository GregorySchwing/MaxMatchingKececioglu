#include <stdio.h>
#include "graph.h"
#include "matching.h"
#include <time.h>
#include <unistd.h>
#include <string.h>
#include <libgen.h>

#include <sys/time.h>
double getTimeOfDay() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec / 1000000.0;
}

void edgeList2MatchingArray(PyObject *matched_edges, int * matching){
    // Assuming matched_edges is a Python list object
    for (Py_ssize_t i = 0; i < PyList_Size(matched_edges); ++i) {
        // Get the i-th tuple from the list
        PyObject* tuple = PyList_GetItem(matched_edges, i);
        if (tuple == NULL || !PyTuple_Check(tuple)) {
            printf("Error: Failed to get tuple from list or not a tuple\n");
            continue;
        }

        // Extract elements from the tuple
        PyObject* element1 = PyTuple_GetItem(tuple, 0);
        PyObject* element2 = PyTuple_GetItem(tuple, 1);

        // Check if extraction was successful
        if (element1 == NULL || element2 == NULL) {
            printf("Error: Failed to get elements from tuple\n");
            continue;
        }

        // Convert elements to integers (or desired type)
        long value1 = PyLong_AsLong(element1);
        long value2 = PyLong_AsLong(element2);

        // Check for conversion errors
        if (value1 == -1 || value2 == -1) {
            PyErr_Print();  // Print Python error message
            printf("Error: Failed to convert elements to integers\n");
            continue;
        }

        // Now, you can use value1 and value2 as needed
        #ifndef NDEBUG
        printf("Tuple %zd: (%ld, %ld)\n", i, value1, value2);
        #endif
        matching[value1]=value2;
        matching[value2]=value1;
    }
}

// Function to clear a Python list
void clearList(PyObject* list) {
    PyList_SetSlice(list, 0, PyList_Size(list), NULL);
}

typedef ListCell Cell;
int main(int argc, char **argv){}
void match (PyObject *rows, PyObject *cols, PyObject *matching)
{

   int   N;
   List *M;
   Cell *P;
   

   Graph  *G;
   Vertex *V;
   Edge   *E;
   int *matching_array;
   // Function logic for the first list
   Py_ssize_t rows_length = PyList_Size(rows);
   Py_ssize_t cols_length = PyList_Size(cols);
   Py_ssize_t matching_length = PyList_Size(matching);

   int nr = rows_length-1;
   int nc = rows_length-1;
   int nn = cols_length;
   //int * rows;
   //int * cols;
   //int * matching;
   double start_time_wall, end_time_wall;
   double start_time_csc_2_g, end_time_csc_2_g;
   double start_time_match, end_time_match;
   start_time_wall = getTimeOfDay();
   start_time_csc_2_g = getTimeOfDay();
   if (matching_length){
        // Number of elements in the array
        size_t num_elements = nr;

        // Size of each element in bytes
        size_t element_size = sizeof(int);

        // Allocate memory for the array and initialize to zero
        matching_array = (int *)calloc(num_elements, element_size);
        edgeList2MatchingArray(matching,matching_array);
        // Clear the list
        clearList(matching);
   } else {
    matching_array = 0x0;
   }
   G = CreateGraphFromCSC(rows, cols, matching_array, nr, nc, nn, !matching_length);
   if (matching_length)
    free(matching_array);
   end_time_csc_2_g = getTimeOfDay();
   printf("CSC to Graph conversion time: %f seconds\n", end_time_csc_2_g - start_time_csc_2_g);
   #ifndef NDEBUG
   const char* extensionX = ".augP";
   char outputFilenameX[500];
   strcpy(outputFilenameX, argv[1]);
   strcat(outputFilenameX, extensionX);
   const char* extensionY = ".augT";
   char outputFilenameY[500];
   strcpy(outputFilenameY, argv[1]);
   strcat(outputFilenameY, extensionY);
   const char* extensionZ = ".dead";
   char outputFilenameZ[500];
   strcpy(outputFilenameZ, argv[1]);
   strcat(outputFilenameZ, extensionZ);
   FILE *output_fileX;
   FILE *output_fileY;
   FILE *output_fileZ;
   output_fileX = fopen(outputFilenameX, "w");
   output_fileY = fopen(outputFilenameY, "w");
   output_fileZ = fopen(outputFilenameZ, "w");
   #endif

   #ifndef NDEBUG
   M = MaximumCardinalityMatchingTrack(G,output_fileX,output_fileY,output_fileZ);
   fclose(output_fileX);
   fclose(output_fileY);
   fclose(output_fileZ);
   #endif
   // Record the starting time
   start_time_match = getTimeOfDay();
   M = MaximumCardinalityMatching(G);
   end_time_match = getTimeOfDay();
   end_time_wall = getTimeOfDay();

   printf("Match time: %f seconds\n", end_time_match - start_time_match);


   // Calculate and print the elapsed time
   printf("Total Wall time: %f seconds\n", end_time_wall - start_time_wall);
   fprintf(stdout, "There are %d edges in the maximum-cardinality matching.\n",
           ListSize(M));
   const Py_ssize_t tuple_length = 2;
   if(matching == NULL) {
    printf("Error building pylist\n");
   }
   N = 1;
   ForAllGraphVertices(V, G, P)
      VertexRelabel(V, (VertexData) N++);
   ForAllEdges(E, M, P){
        PyObject *the_tuple = PyTuple_New(tuple_length);
        if(the_tuple == NULL) {
            printf("Error building py object tuple\n");
        }
        //PyObject *the_object1 = PyLong_FromSsize_t((int)VertexLabel(EdgeFrom(E)));
        PyObject *the_object1 = PyLong_FromSsize_t((long)VertexLabel(EdgeFrom(E)));
        
        if(the_object1 == NULL) {
            printf("Error building py object\n");
        }
        //PyObject *the_object2 = PyLong_FromSsize_t((int)VertexLabel(EdgeTo(E)));
        PyObject *the_object2 = PyLong_FromSsize_t((long)VertexLabel(EdgeTo(E)));
        if(the_object2 == NULL) {
            printf("Error building py object\n");
        }
        PyTuple_SET_ITEM(the_tuple, 0, the_object1);
        PyTuple_SET_ITEM(the_tuple, 1, the_object2);
        if(PyList_Append(matching, the_tuple) == -1) {
            printf("Error appending py tuple object\n");
        }
        //fprintf(stdout, "Appended (%d, %d)\n",(int) VertexLabel(EdgeFrom(E)), (int) VertexLabel(EdgeTo(E)));
        #ifndef NDEBUG
        fprintf(stdout, "Appended (%ld, %ld)\n",(long) VertexLabel(EdgeFrom(E)), (long) VertexLabel(EdgeTo(E)));
        #endif
   }
      
      //fprintf(stdout, "(%d, %d)\n",(int) VertexLabel(EdgeFrom(E)), (int) VertexLabel(EdgeTo(E)));
      
   
   DestroyList(M);
   
   DestroyGraph(G);
   return;
}
