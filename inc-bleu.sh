#!/bin/bash

# This calculates BLEU score by filtering
# the phrases incrementally like:
# 1st word reference & hypothesis
# 1st and 2nd word reference % hypothesis, etc.
#
# You have to have multi-bleu.perl in your $PATH

# Tokenized Reference translations
REF=$1

# Tokenized translation hypotheses
HYP=$2

# Cutoff value to stop
MAX=10

for i in `seq $MAX`; do
  echo "Words: 1-$i"
  echo "----------------------"
  multi-bleu.perl <(cut -d" " -f1-$i $REF) < <(cut -d" " -f1-$i $HYP)
  echo
done
