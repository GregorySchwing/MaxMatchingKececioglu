#!/bin/bash

C=10
C=2
cr=0.99  # Integer representation of 0.42
for C in {2..10}
do
for i in {5..5}
do
for j in {1..5}
do
a=42  # Integer representation of 0.42
b=10  # Integer representation of 0.10
o=44  # Integer representation of 0.44
ab=4   # Integer representation of 0.04
let UNSCALEDV=10**$i   # sets SCALE to 10Ei.
VERTICES=$(($UNSCALEDV*$j))
EDGES=$(($C*$VERTICES))
filenameKece="${VERTICES}_${EDGES}_o${o}_a${a}_b${b}_ab${ab}.KPD.txt"
filenameMTX="${filenameKece}.mtx"
#python kidney.py -N $VERTICES -M $EDGES -output $filenameKece --O_prob $o --A_prob $a --B_prob $b --AB_prob $ab
python kidney_parallel.py -N $VERTICES -M $EDGES -output $filenameKece --O_prob $o --A_prob $a --B_prob $b --crossmatch_prob $cr
echo $filenameKece
echo $filenameMTX

../../src/matching $filenameKece
/home/greg/mvm/src/cpu $filenameMTX
#/home/greg/mvm/src/a.out $filenameMTX 0 1
/home/greg/mvm/src/a.out $filenameMTX 60 48
rm $filenameMTX
rm $filenameKece
done
done
done

a=42  # Integer representation of 0.42
b=10  # Integer representation of 0.10
o=44  # Integer representation of 0.44
ab=4   # Integer representation of 0.04
