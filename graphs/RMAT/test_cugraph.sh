#!/bin/bash


C=10
for j in {4..6}
do
let VERTICES=2**$j   # sets SCALE to 10Ei.
EDGES=$(($VERTICES*$C))
filename="${VERTICES}_${EDGES}_RMAT.txt"
a=0.45
b=0.22
c=0.22
python generate_rmat_graph.py $j $EDGES $a $b $c $filename true
echo "Calling ../../src/matching $filename"
../../src/matching $filename
rm $filename
#cp $filenameShifted $filenameBlossV
#sed -i -e 's/^/e /' $filenameBlossV
#sed -i -e 's/$/ 1/' -i $filenameBlossV
#sed -i "1s/^/p edge $VERTICES $EDGES\n/" $filenameBlossV
#../../blossom5-v2.04.src/blossom5 -e $filenameBlossV
done

