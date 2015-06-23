#!/bin/bash

for INFILE in "$@"
do
    OUT=${INFILE%.xml}.txt
    echo "$INFILE -> $OUT"
    sed -n "/^<seg id/s/^<seg id.*> \(.*\) <\/seg>.*$/\1/gp" < $INFILE > $OUT
done
