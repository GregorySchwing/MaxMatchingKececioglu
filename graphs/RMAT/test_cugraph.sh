#!/bin/bash


C=10
for i in {5..5}
do
for j in {5..20}
do
let VERTICES=2**$i   # sets SCALE to 10Ei.
EDGES=$(($VERTICES*$C))
filename="${VERTICES}_${EDGES}_RMAT.txt"
a=0.45
b=0.22
c=0.22
python generate_rmat_graph.py $j $EDGES $a $b $c $filename 1
../../src/matching $filenameKece
rm $filenameKece
#cp $filenameShifted $filenameBlossV
#sed -i -e 's/^/e /' $filenameBlossV
#sed -i -e 's/$/ 1/' -i $filenameBlossV
#sed -i "1s/^/p edge $VERTICES $EDGES\n/" $filenameBlossV
#../../blossom5-v2.04.src/blossom5 -e $filenameBlossV


done
done
