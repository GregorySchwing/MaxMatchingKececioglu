#!/bin/bash


C=10
k=0.3
for deg in 2 3 5 10
do
for i in {5..5}
do
for j in {1..20}
do
let SCALE=10**$i   # sets SCALE to 10Ei.
VERTICES=$(($j*$SCALE))
filename="${VERTICES}_${deg}_WS.txt"
python generate_watts_strogatz_grap_cugraph2.py $VERTICES $deg $k $filename
../MaxMatchingKececioglu/src/matching $filename
rm $filename
done
done
done
