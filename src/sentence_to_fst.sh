#!/bin/bash
#
# Convert a sentence to an equivalent FST in the AT&T FSM format.

function sentence_to_fst() {

    local IFS=' '
    local state=0
    local sentence=($1)
    local last_index=`expr ${#sentence[@]} - 1`

    for i in "${!sentence[@]}"; do
        if (( i < last_index )); then
            local j=`expr $i + 1`
            printf "%s %s %s %s\n" "$i" "$j" "${sentence[$i]}" "${sentence[$j]}"
        else
            printf "%s\n" "$i"
        fi
    done

}

if [ $# -ne 0 ]; then
    if [ $# -eq 1 ]; then
        sentence_to_fst "$1"
    else
        echo "usage: sentence_to_fst sentence"
        exit -1
    fi
fi
