#!/bin/bash
#
# Convert a sentence to an equivalent FST in the AT&T FSM format.

function sentence_to_osyms() {

    local IFS=' '
    local state=0
    local sentence=($1)
    local last_index=`expr ${#sentence[@]} - 1`

    printf "<eps> 0\n"

    for i in "${!sentence[@]}"; do
        local j=`expr $i + 1`
        printf "%s %s\n" "${sentence[$i]}" "$j"
    done

}

if [ $# -ne 0 ]; then
    if [ $# -eq 1 ]; then
        sentence_to_osyms "$1"
    else
        echo "usage: sentence_to_osyms sentence"
        exit -1
    fi
fi
