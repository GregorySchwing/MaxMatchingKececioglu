#!/bin/bash


C=2
Clist=(2 3 5 10 15 20 30 40 50 60 70 80 90 100)
for repl in {1..5}
do
for C in ${Clist[@]}
do
for i in {5..5}
do
for j in {1..5}
do
let SCALE=10**$i   # sets SCALE to 10Ei.
VERTICES=$(($j*$SCALE))
EDGES=$(($VERTICES*$C))
filename="${VERTICES}_${EDGES}_${C}_RMAT.txt"
filenameShifted="${filename}_start_from_1.txt"
filenameKece="${VERTICES}_${EDGES}_${C}_RMAT_Kece.txt"
filenameBlossV="${VERTICES}_${EDGES}_${C}_RMAT_blossV.txt"
filenameMTX="${VERTICES}_${EDGES}_${C}_RMAT.txt.mtx"
../PaRMAT/Release/PaRMAT -nVertices ${VERTICES} -nEdges ${EDGES} -output $filename -threads 16 -sorted -noEdgeToSelf -noDuplicateEdges -undirected -a 0.45 -b 0.15 -c 0.15 -d 0.25

awk -v s=1 '{print $1+s, $2+s}' $filename > $filenameShifted

cp $filenameShifted $filenameKece
cp $filenameShifted $filenameMTX
rm $filename
rm $filenameShifted
sed -i -e 's/^/edge /' $filenameKece
sed -i "1s/^/vertices $VERTICES\n/" $filenameKece
sed -i "2s/^/edges $EDGES\n/" $filenameKece
#../../src/matching $filenameKece
rm $filenameKece

sed -i "1s/^/%%MatrixMarket matrix coordinate pattern symmetric\n/" $filenameMTX
sed -i "2s/^/$VERTICES $VERTICES $EDGES\n/" $filenameMTX

#cp $filenameShifted $filenameBlossV
#sed -i -e 's/^/e /' $filenameBlossV
#sed -i -e 's/$/ 1/' -i $filenameBlossV
#sed -i "1s/^/p edge $VERTICES $EDGES\n/" $filenameBlossV
#../../blossom5-v2.04.src/blossom5 -e $filenameBlossV

/home/greg/mvm/src/cpu $filenameMTX
/home/greg/mvm/src/a.out $filenameMTX 0 1
/home/greg/mvm/src/a.out $filenameMTX 60 48
/home/greg/mvm/src/a.out $filenameMTX 60 32
rm $filenameMTX


done
done
done
done
