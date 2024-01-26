git submodule update --init --recursive
git submodule update --recursive --remote
cd src
make

USE:
Wrapper args: a,b
a: ALGO [0: MS-BFS-GRAFT; 1: matchmaker2]
b: JUST READ FILE - CONTROL [0: False, 1: True]
c: Filename (NOTE, this cannot be too long or buffer overflows)
MS-BFS args: d,e
d: Num Threads
e: KarpSipser Initialization [0: Serial, 1: Parallel]
matchmaker2 args:
d: Match type (variety of options)
e: Initial Match Type

        MT: Maximum Matching Type
                0: Sequential DFS
                1: Sequential BFS
                2: Sequential PF
                3: Sequential PFP
                4: Sequential HK
                5: Sequential HK_DW
                6: Sequential ABMP
                7: Sequential ABMP_BFS
                8: GPU - APFB_GPUBFS
                9: GPU - APFB_GPUBFS_WR
                10: GPU - APsB_GPUBFS
                11: GPU - APsB_GPUBFS_WR
        IMT: Initial Matching Type
                0: 
                0: Cheap Matching
                1: SK
                2: SK_rand
                3: mind_cheap
                >=4: no initial matching

binary     a b c                                       d  e
./matching 0 0 ../graphs/test_cases/luxembourg_osm.mtx 16 1
./matching 0 1 ../graphs/test_cases/luxembourg_osm.mtx 16 1
binary     a b c                                           d      e
./matching 1 0 IF=../graphs/test_cases/luxembourg_osm.mtx  MT=9   IMT=0
./matching 1 1 IF=../graphs/test_cases/luxembourg_osm.mtx  MT=9   IMT=0  
