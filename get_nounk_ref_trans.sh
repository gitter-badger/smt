#!/bin/bash

# Filters out source phrases containing <unk>'s and their
# related hypotheses.
REF=$1
CSTM_EXTRACT=$2

egrep -v "<unk>" $2 | sed "s/^.* ||| //g" > ${CSTM_EXTRACT/extract/nounk}

rm $REF.nounk
for i in `egrep -n -v "<unk>" $2 | cut -d":" -f1`; do
  sed -n "$i"p $REF >> $REF.nounk
done

