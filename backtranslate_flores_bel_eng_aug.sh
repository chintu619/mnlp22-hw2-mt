#!/bin/bash

set -euo pipefail

augID=$1
augID_pre=$2

if [[ -z $FAIRSEQ_DIR ]]; then
  echo "\$FAIRSEQ_DIR enviromental variable needs to be set"
  exit 1
fi

FLORES_MODEL=checkpoints/flores101_mm100_175M
SPM_MODEL=$FLORES_MODEL/sentencepiece.bpe.model
DICT_FILE=$FLORES_MODEL/dict.txt

RAW_DDIR=data/ted_raw_aug/
PROC_DDIR=data/ted_processed/bel_spm_flores_aug${augID}/
PROC_DDIR_PRE=data/ted_processed/bel_spm_flores_aug${augID_pre}/
BINARIZED_DDIR=data/ted_binarized/bel_flores_aug${augID}/

FAIR_SCRIPTS=$FAIRSEQ_DIR/scripts
SPM_TRAIN=$FAIR_SCRIPTS/spm_train.py
SPM_ENCODE=$FAIR_SCRIPTS/spm_encode.py

LANGS=(bel)

for i in ${!LANGS[*]}; do
  LANG=${LANGS[$i]}
  mkdir -p "$PROC_DDIR"/"$LANG"_eng

  LANG_CODE=${LANG:0:2}

  echo "encoding monolingual data with learned BPE..."
  python "$SPM_ENCODE" \
    --model=$SPM_MODEL \
    --output_format=piece \
    --inputs "$RAW_DDIR"/"$LANG"_eng/ted-train.mono-QED."$LANG" "$RAW_DDIR"/"$LANG"_eng/ted-train.mono-QED.eng  \
    --outputs "$PROC_DDIR"/"$LANG"_eng/ted-test.spm."$LANG_CODE" "$PROC_DDIR"/"$LANG"_eng/ted-test.spm.en

  # -- fairseq binarization ---
  echo "Binarize the data... (bel-eng)"
  fairseq-preprocess --source-lang $LANG_CODE --target-lang en \
	  --srcdict $DICT_FILE --tgtdict $DICT_FILE --thresholdsrc 0 --thresholdtgt 0 \
	  --trainpref "$PROC_DDIR_PRE"/"$LANG"_eng/ted-train.spm \
	  --validpref "$PROC_DDIR_PRE"/"$LANG"_eng/ted-dev.spm \
	  --testpref "$PROC_DDIR"/"$LANG"_eng/ted-test.spm \
	  --destdir $BINARIZED_DDIR/"$LANG"_eng/
done

RAW_DATA=data/ted_raw_aug/bel_eng/
BINARIZED_DATA=data/ted_binarized/bel_flores_aug${augID}/bel_eng/
PRETRAINED_DIR=checkpoints/flores101_mm100_175M
MODEL_DIR=checkpoints/ted_bel_flores_aug${augID_pre}/bel_eng/
COMET_DIR=comet
mkdir -p $MODEL_DIR

# translate & eval the valid and test set
fairseq-generate $BINARIZED_DATA \
    --gen-subset test \
	--task translation_multi_simple_epoch \
	--source-lang be --target-lang en \
    --path $MODEL_DIR/checkpoint_best.pt \
	--fixed-dictionary $PRETRAINED_DIR/dict.txt \
	--lang-pairs $PRETRAINED_DIR/language_pairs.txt \
	--decoder-langtok --encoder-langtok src \
    --batch-size 224 \
    --remove-bpe sentencepiece \
    --beam 5  | grep ^H | cut -c 3- | sort -n | cut -f3- > "$RAW_DATA"/ted-train.synth-QED.eng

