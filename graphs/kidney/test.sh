#!/bin/bash

C=10

for i in {3..3}
do
for j in {1..10}
do
a=42  # Integer representation of 0.42
b=10  # Integer representation of 0.10
o=44  # Integer representation of 0.44
ab=4   # Integer representation of 0.04
let SCALE=10**$i   # sets SCALE to 10Ei.
VERTICES=$(($j*$SCALE))
EDGES=$(($C*$VERTICES))
filenameKece="${VERTICES}_${EDGES}_o${o}_a${a}_b${b}_ab${ab}.KPD.txt"
filenameMTX="${filenameKece}.mtx"
python kidney.py -N $VERTICES -M $EDGES -output $filenameKece --O_prob $o --A_prob $a --B_prob $b --AB_prob $ab
echo $filenameKece
echo $filenameMTX
exit 1
../../src/matching $filenameKece
/home/greg/mvm/src/cpu $filenameMTX
/home/greg/mvm/src/a.out $filenameMTX 0 1
#/home/greg/mvm/src/a.out $filenameMTX 60 48
#rm $filename
done
done

for i in {3..3}
do
for j in {1..10}
do
a=32  # Integer representation of 0.32
b=31  # Integer representation of 0.31
o=27  # Integer representation of 0.27
ab=10 # Integer representation of 0.10
let SCALE=10**$i   # sets SCALE to 10Ei.
VERTICES=$(($j*$SCALE))
EDGES=$(($C*$VERTICES))
filenameKece="${VERTICES}_${EDGES}_o${o}_a${a}_b${b}_ab${ab}.KPD.txt"
filenameMTX="${filenameKece}.mtx"
python kidney.py -N $VERTICES -M $EDGES -output $filenameKece --O_prob $o --A_prob $a --B_prob $b --AB_prob $ab
../../src/matching $filenameKece
/home/greg/mvm/src/cpu $filenameMTX
/home/greg/mvm/src/a.out $filenameMTX 0 1
#/home/greg/mvm/src/a.out $filenameMTX 60 48
#rm $filename
done
done

