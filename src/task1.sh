#!/bin/bash
#
# Convert the first 100 sentence in data/dev.en to FSTs.

# Set the path to the src/ directory.
#
SRC_DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$SRC_DIR" ]]; then SRC_DIR="$SRC_PWD"; fi

# Set the path to the data/ directory.
#
DATA_DIR=${DATA_DIR:-"$SRC_DIR/../data"}

# Set the path to the dev.en file.
#
DEV_EN=${DEV_EN:-"$DATA_DIR/dev.en"}

# Set the path to the output/ directory.
#
OUT_DIR=${OUT_DIR:-"$DATA_DIR/task1"}

mkdir -p "$OUT_DIR"

# Set the number of sentences to convert to FSTs.
#
N=${N:-"100"}

# Import sentence_to_fst.
#
source "$SRC_DIR/sentence_to_fst.sh"

# Convert the first $N sentences in $DEV_EN to FSTs.
#
IFS=$'\n'
sentences=(`head -n $N $DEV_EN`)
for i in "${!sentences[@]}"; do
    printf "\r$(expr $i + 1)/$N"
    OUT_FILE="$OUT_DIR/dev.en.$i.txt"
    sentence_to_fst "${sentences[$i]}" > $OUT_FILE
done
printf "\r"
