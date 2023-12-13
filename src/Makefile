CC	= gcc

#CFLAGS	= -O3 -DDebug=1
CFLAGS = -fopenmp -Drestrict=__restrict__ -O2 -DNDEBUG -ffast-math # -g -pg

CFLAGS	= -O3 -DNDEBUG -I/usr/include/python3.8 -lpython3.8

RM   = rm -f
SHAR = shar
LINT = lint -x

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SOURCES = driver.c matching.c graph.c list.c set.c
OBJECTS = driver.o matching.o graph.o list.o set.o

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# -dc is the flag for separate compilation. 
# The architecture must be specified before -dc see (with a generic Makefile).


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#matching : ${OBJECTS}
#	${CC} ${CFLAGS} -o matching ${OBJECTS}
all: matching

matching : ${OBJECTS}
	${CC} ${CFLAGS} -o matching ${OBJECTS} -lpython3.8
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

clean :
	${RM} *.o Makefile.bak core

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
