#!/bin/bash
#
# Convert a phrase-table to an equivalent FST in the AT&T FSM format.

function strip_space() {
    echo `sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]+/ /' -e 's/[[:space:]]*$//' <<< "$1"`
}

function phrasetable_to_fst() {

    local IFS=$'\n'
    local state=0
    local rules=(`cat "$1"`)

    for rule in "${rules[@]}"; do

        # WARN: this will FAIL if there are any |'s present in the remainder of
        # the line, since IFS separates by CHARACTER
        local IFS=$'|||'
        local rule=($rule)

        local IFS=$' '
        local source=(`strip_space "${rule[3]}"`)
        local target=(`strip_space "${rule[6]}"`)
        local feature_map=(`strip_space "${rule[9]}"`)
        local last_index=`expr ${#target[@]} - 1`

        if (( ${#source[@]} == 1 )) && (( ${#target[@]} == 1 )); then

            printf "0 0 %s %s\n" "${source[@]}" "${target[@]}"

        else

            # Set state to the first _fresh_ state.
            state=`expr $state + 1`

            # Delete the source phrase.
            for i in "${!source[@]}"; do

                next_state=`expr $state + 1`
                if (( $i == 0 )); then
                    printf "0 %s %s %s\n" "$state" "${source[$i]}" "<eps>"
                else
                    printf "%s %s %s %s\n" "$state" "$next_state" "${source[$i]}" "<eps>"
                fi
                state="$next_state"

            done

            # Insert the target phrase.
            for j in "${!target[@]}"; do

                next_state=`expr $state + 1`
                if (( $j < $last_index )); then
                    printf "%s %s %s %s\n" "$state" "$next_state" "<eps>" "${target[$j]}"
                else
                    printf "%s 0 %s %s\n" "$state" "<eps>" "${target[$j]}"
                fi
                state="$next_state"

            done
        fi
    done
}

if [ $# -ne 0 ]; then
    if [ $# -eq 1 ]; then
        phrasetable_to_fst "$1"
    else
        echo "usage: phrasetable_to_fst grammar_file"
        exit -1
    fi
fi
