#!/usr/bin/env bash
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
RULES_MONOTONE_DEV=${RULES_MONOTONE_DEV:-"$DATA_DIR/rules.monotone.dev"}

# Set the path to the output/ directory.
#
OUT_DIR=${OUT_DIR:-"$DATA_DIR/task2"}

mkdir -p "$OUT_DIR"

# Set the number of sentences to convert to FSTs.
#
N=${N:-"100"}

# Import dependencies.
#
source "$SRC_DIR/phrasetable_to_fst.sh"

k=4
phrasetable_to_fst "$RULES_MONOTONE_DEV/grammar.$k"
