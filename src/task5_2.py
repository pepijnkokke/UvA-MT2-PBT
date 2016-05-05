#!/usr/bin/env python
#
# Convert the first 100 grammars in data/rules.monotone.dev to FSTs.

from task1 import mkdir_p


import itertools
import math
import os
import subprocess
import sys


def parse_sentences(fi):

    def parse_lattice(l):
        (_, feature_list, indices, tokens) = l.split('|||')

        feature_map = dict()
        for feature in feature_list.split():
            key, value = feature.split('=')
            feature_map[key] = float(value)

        indices = [int(x) for x in indices.split()]
        tokens = tokens.split()

        return tokens, indices, feature_map

    return [
        [parse_lattice(l) for l in s.split('\n') if len(l.split('|||')) == 4]
        for s in fi.read().split('\n\n')
    ]


def phrasetable_to_ovv(sentence, phrasetable):
    """ Convert a phrase-table to a list of all OVV words. """

    words_with_rules = [
        rule.split('|||')[1].strip()
        for rule in phrasetable]

    words_without_rules = [
        word for word in sentence[0][0]
        if not (word in words_with_rules)]

    return set(words_without_rules)


def phrasetable_to_osyms(sentence, phrasetable, os = sys.stdout):
    """ Convert a phrase-table to a symbol table for its output labels. """

    words_with_rules = set(itertools.chain(*[
        rule.split('|||')[2].split()
        for rule in phrasetable]))

    words_with_rules |= phrasetable_to_ovv(sentence, phrasetable)

    os.write("<epsilon> 0\n")

    for i, w in enumerate(words_with_rules):
        os.write("{} {}\n".format(w, i + 1))



def phrasetable_to_fst(sentence, phrasetable, weight_map, os = sys.stdout):
    """ Convert a phrase-table to an FST in the AT&T format. """

    curr_state = 0

    for rule in phrasetable:
        (_, source, target, feature_list, _) = rule.split('|||')

        source = source.split()
        target = target.split()

        # Compute the feature map.
        feature_map = dict()
        for feature in feature_list.split():
            key, value = feature.split('=')
            feature_map[key] = float(value) * weight_map[key]

        feature_map['Glue'] = weight_map['Glue']
        feature_map['WordPenalty'] = -1/math.log(10) * len(target) * weight_map['WordPenalty']

        # Sum all features to compute the weight.
        weight = sum(feature_map.values())

        last_index = len(target) - 1

        if len(source) == 1 and len(target) == 1:

            os.write("0 0 {} {} {}\n".format(source[0], target[0], weight))

        else:

            curr_state = curr_state + 1

            # Delete the source phrase.
            for i in range(0, len(source)):

                if i == 0:
                    os.write("0 {} {} <epsilon> {}\n".
                             format(curr_state, source[i], weight))
                else:
                    next_state = curr_state + 1
                    os.write("{} {} {} <epsilon> 0\n".
                             format(curr_state, next_state, source[i]))
                    curr_state = next_state

            # Insert the target phrase.
            for j in range(0, len(target)):
                next_state = curr_state + 1
                if j < last_index:
                    os.write("{} {} <epsilon> {} 0\n".
                             format(curr_state, next_state, target[j]))
                else:
                    os.write("{} 0 <epsilon> {} 0\n".
                             format(curr_state, target[j]))

                curr_state = next_state


    # Generate OVV rules.
    words_without_rules = phrasetable_to_ovv(sentence, phrasetable)

    for word in words_without_rules:
        os.write("0 0 {0} {0} {1}\n".format(word, weight_map['PassThrough']))

    os.write("0\n")


if __name__ == "__main__":

    # Set the path to the src/, data/ and out/ directories.
    src_dir  = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.getenv('DATA_DIR',os.path.join(os.path.join(src_dir,'..'),'data'))
    out_dir = os.getenv('OUT_DIR', os.path.join(os.path.join(src_dir, '..'), 'out'))

    task5_1_out_dir = os.path.join(out_dir, 'task5.1')
    task5_2_out_dir = os.path.join(out_dir, 'task5.2')

    # Make sure the out/ directory exists.
    mkdir_p(task5_2_out_dir)

    # Set the path to the input file (dev.en).
    dev_en             = os.getenv('DEV_EN',
                                   os.path.join(data_dir,'dev.enpp.nbest'))
    weights_lattice   = os.getenv('WEIGHTS_MONOTONE',
                                   os.path.join(data_dir,'weights.lattice'))
    rules_nbest_dev = os.getenv('RULES_MONOTONE_DEV',
                                   os.path.join(data_dir,'rules.n-best.dev'))

    # Set the number of sentences to convert to FSTs.
    s = os.getenv('S', 1316)
    n = os.getenv('N', 100)

    # Read the first N entries from DEV_EN.
    with open(dev_en, 'r') as f:
        sentences = parse_sentences(f)[s:s+n]

    # Read the weights.
    with open(weights_lattice, 'r') as f: weight_list = f.readlines()
    weight_map = dict()
    for weight in weight_list:
        weight = weight.split()
        weight_map[weight[0]] = float(weight[1])

    # Iterate over the sentences, read the appropriate phrase table,
    # and generate an FST.
    for i, sentence in enumerate(sentences):

        if i >= n:
            break

        j = i + s

        sys.stdout.write("\r{}/{}".format(i + 1, n))
        sys.stdout.flush()

        grammar_file = os.path.join(rules_nbest_dev,'grammar.{}'.format(j))
        with open(grammar_file, 'r') as f:
            phrasetable = f.readlines()

        osyms_file = os.path.join(task5_2_out_dir,'dev.ja.{}.osyms'.format(j))
        with open(osyms_file, 'w') as f:
            phrasetable_to_osyms(sentence, phrasetable, f)

        fst_txt_file = os.path.join(task5_2_out_dir,'grammar.{}.fst.txt'.format(j))
        with open(fst_txt_file, 'w') as f:
            phrasetable_to_fst(sentence, phrasetable, weight_map, f)

        fst_file = os.path.join(task5_2_out_dir,'grammar.{}.fst'.format(j))
        isyms_file = os.path.join(task5_1_out_dir,'dev.en.{}.osyms'.format(j))
        subprocess.call(['fstcompile',
                         '--keep_isymbols', '--keep_osymbols',
                         '--isymbols={}'.format(isyms_file),
                         '--osymbols={}'.format(osyms_file),
                         fst_txt_file,fst_file])
        subprocess.call(['fstarcsort',
                         '--sort_type=ilabel',
                         fst_file,fst_file])
        #
        # dot_file = os.path.join(task5_2_out_dir, 'grammar.{}.dot'.format(j))
        # subprocess.call(['fstdraw',
        #                  '--portrait=true',
        #                  fst_file, dot_file])
        #
        # png_file = os.path.join(task5_2_out_dir, 'grammar.{}.png'.format(j))
        # subprocess.call(['dot', '-Tpng', '-Gdpi=3000', dot_file, '-o', png_file])

    sys.stdout.write("\r")
    sys.stdout.flush()
