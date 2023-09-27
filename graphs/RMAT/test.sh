#!/bin/bash


C=10
for i in {5..5}
do
for j in {1..20}
do
let SCALE=10**$i   # sets SCALE to 10Ei.
VERTICES=$(($j*$SCALE))
EDGES=$(($VERTICES*$C))
filename="${VERTICES}_${EDGES}_RMAT.txt"
filenameShifted="${VERTICES}_${EDGES}_RMAT_start_from_1.txt"
filenameKece="${VERTICES}_${EDGES}_RMAT_Kece.txt"
filenameBlossV="${VERTICES}_${EDGES}_RMAT_blossV.txt"
../Release/PaRMAT -nVertices ${VERTICES} -nEdges ${EDGES} -output $filename -threads 16 -sorted -noEdgeToSelf -noDuplicateEdges -undirected

awk -v s=1 '{print $1+s, $2+s}' $filename > $filenameShifted

cp $filenameShifted $filenameKece
rm $filename
rm $filenameShifted
sed -i -e 's/^/edge /' $filenameKece
sed -i "1s/^/vertices $VERTICES\n/" $filenameKece
sed -i "2s/^/edges $EDGES\n/" $filenameKece
../../MaxMatchingKececioglu/src/matching $filenameKece
rm $filenameKece
#cp $filenameShifted $filenameBlossV
#sed -i -e 's/^/e /' $filenameBlossV
#sed -i -e 's/$/ 1/' -i $filenameBlossV
#sed -i "1s/^/p edge $VERTICES $EDGES\n/" $filenameBlossV
#../../blossom5-v2.04.src/blossom5 -e $filenameBlossV


done
done
