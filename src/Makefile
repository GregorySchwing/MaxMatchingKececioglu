CC	= gcc
NVCC = nvcc

#CFLAGS	= -O3 -DDebug=1
CFLAGS	= -O3 -DNDEBUG
CUDAFLAGS = -O3 -Xptxas -O3 -Xcompiler -O3 -w 

RM   = rm -f
SHAR = shar
LINT = lint -x

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SOURCES = driver.c matching.c graph.c list.c set.c hash_table.c bipartite.cu matchgpu.cu CSRGraph.cu GreedyMatcher.cu\
bfs.cu
OBJECTS = driver.o matching.o graph.o list.o set.o hash_table.o bipartite.o matchgpu.o CSRGraph.o GreedyMatcher.o\
bfs.o

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# -dc is the flag for separate compilation. 
# The architecture must be specified before -dc see (with a generic Makefile).

%.o: %.cu
	${NVCC} -dc $(CUDAFLAGS) $< -o $@

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#matching : ${OBJECTS}
#	${CC} ${CFLAGS} -o matching ${OBJECTS}

matching : ${OBJECTS}
#	${CC} ${CFLAGS} -o matching ${OBJECTS}
	${NVCC} -o matching ${OBJECTS}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

clean :
	${RM} *.o Makefile.bak core

shar :
	${SHAR} Makefile Notes Version Example *.c *.h > matching.sh

lint :
	${LINT} ${SOURCES}

depend :
	makedepend ${SOURCES}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# DO NOT DELETE THIS LINE -- make depend depends on it.

driver.o: /usr/include/stdio.h feature_tests.h graph.h
driver.o: portable.h /usr/include/stdlib.h list.h matching.h
matching.o: /usr/include/stdio.h feature_tests.h matching.h
matching.o: list.h portable.h /usr/include/stdlib.h graph.h set.h
graph.o: /usr/include/stdio.h feature_tests.h graph.h
graph.o: portable.h /usr/include/stdlib.h list.h
list.o: /usr/include/stdio.h feature_tests.h list.h
list.o: portable.h /usr/include/stdlib.h
set.o: /usr/include/stdio.h feature_tests.h set.h portable.h
set.o: /usr/include/stdlib.h
