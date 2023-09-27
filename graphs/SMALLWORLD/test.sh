#!/bin/bash


C=10
p=0.3
for degDenom in 10 5 2 1
do
for i in {5..5}
do
for j in {1..20}
do
let SCALE=10**$i   # sets SCALE to 10Ei.
VERTICES=$(($j*$SCALE))
filename="${VERTICES}_${deg}_WS.txt"
deg=$((VERTICES / degDenom))
python generate_watts_strogatz_graph.py $VERTICES $deg $p $filename 0
../../src/matching $filename
rm $filename
done
done
done
