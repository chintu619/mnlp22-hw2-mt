#!/bin/bash

set -euo pipefail

if [[ -z $FAIRSEQ_DIR ]]; then
  echo "\$FAIRSEQ_DIR enviromental variable needs to be set"
  exit 1
fi

FLORES_MODEL=checkpoints/flores101_mm100_175M
SPM_MODEL=$FLORES_MODEL/sentencepiece.bpe.model
DICT_FILE=$FLORES_MODEL/dict.txt

RAW_DDIR=data/ted_raw/
PROC_DDIR=data/ted_processed/beltrf_spm_flores/
BINARIZED_DDIR=data/ted_binarized/beltrf_flores/

FAIR_SCRIPTS=$FAIRSEQ_DIR/scripts
SPM_TRAIN=$FAIR_SCRIPTS/spm_train.py
SPM_ENCODE=$FAIR_SCRIPTS/spm_encode.py

LANGS=(bel rus ukr bul)

# for i in ${!LANGS[*]}; do
#   LANG=${LANGS[$i]}
  # if [[ ${LANG} != "tur" ]] 
  # then
		# LANG_CODE=${LANG:0:2}
  # else
		# LANG_CODE="tr"
  # fi 
#   echo ${LANG}
#   echo ${LANG_CODE}
# done
for i in ${!LANGS[*]}; do
  LANG=${LANGS[$i]}
  mkdir -p "$PROC_DDIR"/"$LANG"_eng
  for f in "$RAW_DDIR"/"$LANG"_eng/*.orig.*-eng  ; do
    src=`echo $f | sed 's/-eng$//g'`
    trg=`echo $f | sed 's/\.[^\.]*$/.eng/g'`
    if [ ! -f "$src" ]; then
      echo "src=$src, trg=$trg"
      python cut_corpus.py 0 < $f > $src
      python cut_corpus.py 1 < $f > $trg
    fi
  done
  if [[ ${LANG} != "bul" ]] 
  then
		LANG_CODE=${LANG:0:2}
  else
		LANG_CODE="bg"
  fi 
  # --- apply BPE with sentencepiece ---
  python "$SPM_ENCODE" \
	  --model=$SPM_MODEL \
	  --output_format=piece \
	  --inputs "$RAW_DDIR"/"$LANG"_eng/ted-train.orig."$LANG" "$RAW_DDIR"/"$LANG"_eng/ted-train.orig.eng  \
	  --outputs "$PROC_DDIR"/"$LANG"_eng/ted-train.spm."$LANG_CODE" "$PROC_DDIR"/"$LANG"_eng/ted-train.spm.en \
    --min-len 1 --max-len 200 

  echo "encoding valid/test data with learned BPE..."
  for split in dev test;
  do
    python "$SPM_ENCODE" \
	    --model=$SPM_MODEL \
	    --output_format=piece \
	    --inputs "$RAW_DDIR"/"$LANG"_eng/ted-"$split".orig."$LANG" "$RAW_DDIR"/"$LANG"_eng/ted-"$split".orig.eng  \
	    --outputs "$PROC_DDIR"/"$LANG"_eng/ted-"$split".spm."$LANG_CODE" "$PROC_DDIR"/"$LANG"_eng/ted-"$split".spm.en  
  done
done

# Concatenate all the training data from all languages to get combined vocabulary
mkdir -p $BINARIZED_DDIR
mkdir -p $BINARIZED_DDIR/M2O/
mkdir -p $BINARIZED_DDIR/O2M/

for LANG in ${LANGS[@]}; do
  if [[ ${LANG} != "bul" ]] 
  then
    LANG_CODE=${LANG:0:2}
  else
    LANG_CODE="bg"
  fi
  cat $PROC_DDIR/"$LANG"_eng/ted-train.spm."$LANG_CODE" >> $BINARIZED_DDIR/combined-train.src
  cat $PROC_DDIR/"$LANG"_eng/ted-train.spm.en >> $BINARIZED_DDIR/combined-train.eng
done
fairseq-preprocess -s src -t eng \
  --trainpref $BINARIZED_DDIR/combined-train \
  --joined-dictionary \
  --workers 8 \
  --thresholdsrc 0 \
  --thresholdtgt 0 \
  --destdir $BINARIZED_DDIR

for i in ${!LANGS[*]}; do
  # -- fairseq binarization ---
  echo "Binarize the data... (aze-eng)"
  LANG=${LANGS[$i]}
  if [[ ${LANG} != "bul" ]] 
  then
    LANG_CODE=${LANG:0:2}
  else
    LANG_CODE="bg"
  fi
  fairseq-preprocess --source-lang $LANG_CODE --target-lang en \
	  --srcdict $DICT_FILE --tgtdict $DICT_FILE \
      --thresholdsrc 0 --thresholdtgt 0 \
	  --trainpref "$PROC_DDIR"/"$LANG"_eng/ted-train.spm \
	  --validpref "$PROC_DDIR"/"$LANG"_eng/ted-dev.spm \
	  --testpref "$PROC_DDIR"/"$LANG"_eng/ted-test.spm \
	  --destdir $BINARIZED_DDIR/M2O/

  echo "Binarize the data... (eng-aze)"
  fairseq-preprocess --source-lang en --target-lang $LANG_CODE \
	  --srcdict $DICT_FILE --tgtdict $DICT_FILE --thresholdsrc 0 --thresholdtgt 0 \
	  --trainpref "$PROC_DDIR"/"$LANG"_eng/ted-train.spm \
	  --validpref "$PROC_DDIR"/"$LANG"_eng/ted-dev.spm \
	  --testpref "$PROC_DDIR"/"$LANG"_eng/ted-test.spm \
	  --destdir $BINARIZED_DDIR/O2M/
done