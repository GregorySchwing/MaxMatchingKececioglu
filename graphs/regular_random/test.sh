#!/bin/bash


C=10
for deg in 2 3 5 10
do
for i in {3..3}
do
for j in {1..20}
do
let SCALE=10**$i   # sets SCALE to 10Ei.
VERTICES=$(($j*$SCALE))
filenameKece="${VERTICES}_${deg}_REG_RAND.txt"
filenameMTX="${filenameKece}.mtx"
python generate_random_graph.py $VERTICES $deg $filenameKece matrix_market
../../src/matching $filenameKece
/home/greg/mvm/src/cpu $filenameMTX
/home/greg/mvm/src/a.out $filenameMTX
/home/greg/mvm/src/a.out $filenameMTX 60 48
#rm $filename
done
done
done
