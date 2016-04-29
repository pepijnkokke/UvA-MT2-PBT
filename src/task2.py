#!/usr/bin/env python
#
# Convert the first 100 grammars in data/rules.monotone.dev to FSTs.

from task1 import mkdir_p

import os
import sys


def phrasetable_to_fst(phrasetable, weight_map, os = sys.stdout):
    """ Convert a phrase-table to an FST in the AT&T format. """

    curr_state = 0

    for rule in phrasetable:
        (_, source, target, feature_list, _) = rule.split('|||')

        source = source.split()
        target = target.split()

        # Example FeatureMap:
        #
        #   SampleCountF    : 2.47856649559,
        #   MaxLexEgivenF   : 0.811988173389,
        #   IsSingletonF    : 0.0,
        #   IsSingletonFE   : 0.0,
        #   MaxLexFgivenE   : 0.984836531508,
        #   EgivenFCoherent : 0.769551078622,
        #   CountEF         : 1.71600334363
        #
        feature_map = dict()
        for feature in feature_list.split():
            feature = feature.split('=')
            feature_map[feature[0]] = float(feature[1])

        last_index = len(target) - 1

        if len(source) == 1 and len(target) == 1:

            os.write("0 0 {} {}\n".format(source[0], target[0]))

        else:

            curr_state = curr_state + 1

            # Delete the source phrase.
            for i in range(0,len(source)):

                next_state = curr_state + 1
                if i == 0:
                    os.write("0 {} {} <eps>\n".
                             format(curr_state, source[i]))
                else:
                    os.write("{} {} {} <eps>\n".
                             format(curr_state, next_state, source[i]))
                curr_state = next_state

            # Insert the target phrase.
            for j in range(0,len(target)):

                next_state = curr_state + 1
                if j < last_index:
                    os.write("{} {} <eps> {}\n".
                             format(curr_state, next_state, target[j]))
                else:
                    os.write("{} 0 <eps> {}\n".
                             format(curr_state, target[j]))
                curr_state = next_state


if __name__ == "__main__":

    # Set the path to the src/, data/ and out/ directories.
    src_dir  = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.getenv('DATA_DIR',os.path.join(os.path.join(src_dir,'..'),'data'))
    out_dir  = os.getenv('OUT_DIR',os.path.join(data_dir,'task2'))

    # Make sure the out/ directory exists.
    mkdir_p(out_dir)

    # Set the path to the input file (dev.en).
    weights_monotone   = os.getenv('WEIGHTS_MONOTONE',
                                   os.path.join(data_dir,'weights.monotone'))
    rules_monotone_dev = os.getenv('RULES_MONOTONE_DEV',
                                   os.path.join(data_dir,'rules.monotone.dev'))

    # Set the number of sentences to convert to FSTs.
    n = os.getenv('N',100)

    # Read the weights.
    with open(weights_monotone, 'r') as f: weight_list = f.readlines()
    weight_map = dict()
    for weight in weight_list:
        weight = weight.split()
        weight_map[weight[0]] = float(weight[1])

    for i in range(0,n):

        sys.stdout.write("\r{}/{}".format(i + 1, n))
        sys.stdout.flush()

        inp_file = os.path.join(rules_monotone_dev,'grammar.{}'.format(i))
        with open(inp_file, 'r') as f: phrasetable = f.readlines()

        out_file = os.path.join(out_dir,'grammar.{}'.format(i))
        with open(out_file, 'w') as f: phrasetable_to_fst(phrasetable, weight_map, f)

    sys.stdout.write("\r")
    sys.stdout.flush()
