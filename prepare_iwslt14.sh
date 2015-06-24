#!/bin/bash

CORPUS_PREFIX="train.tags"

# This assumes a folder hierarchy:
#   ./downloads/<src-target>  : IWSLT14 files downloaded and extracted for a language pair
#
# The script will create:
#   ./raw                     : Cleaned text files of test and dev XML's and parallel corpora
#   ./preprocessed            : All the files created by the script preprocess_corpus
#
# At the end, the files in the preprocessed folder can directly be used with CSTM.

TASK=$(basename `pwd`)
echo "Preparing $TASK"

SRC_LANG=`echo $TASK | cut -d"-" -f1`
TGT_LANG=`echo $TASK | cut -d"-" -f2`


if [ ! -d raw ]; then
  mkdir raw
  pushd raw
  # These are dev and test XML files
  # It is possible that they don't contain same talks.
  nistxml2raw.sh ../downloads/IWSLT*xml

  # Get rid of HTML tags in the parallel corpora
  egrep -v "^<.*>" ../downloads/${CORPUS_PREFIX}.${TASK}.${SRC_LANG} > ${CORPUS_PREFIX}.${TASK}.${SRC_LANG}
  egrep -v "^<.*>" ../downloads/${CORPUS_PREFIX}.${TASK}.${TGT_LANG} > ${CORPUS_PREFIX}.${TASK}.${TGT_LANG}

  popd
fi

if [ ! -d preprocessed ]; then
  mkdir preprocessed
  pushd preprocessed

  # This script comes from ~/git/smt (github)
  preprocess_corpus ../raw/${CORPUS_PREFIX}.${TASK}.${SRC_LANG} ../raw/${CORPUS_PREFIX}.${TASK}.${TGT_LANG}

  popd
fi
