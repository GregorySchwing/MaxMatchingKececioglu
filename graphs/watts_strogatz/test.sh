#!/bin/bash
C=10
for i in {5..5}
do
for j in {1..20}
do
for deg in 2 3 5 10
do
for p in {0..10}
do
let SCALE=10**$i   # sets SCALE to 10Ei.
VERTICES=$(($j*$SCALE))
filename="${VERTICES}_${deg}_${p}_WS.txt"
python generate_watts_strogatz_graph.py $VERTICES $deg $p $filename 0
../../src/matching $filename
rm $filename
done
done
done
done
