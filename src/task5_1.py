#!/usr/bin/env python
#
# Convert the first 100 sentence in data/dev.en to FSTs.
#
# Options:
#
#  * DATA_DIR - the data/ directory
#  * OUT_DIR  - the output directory (defaults to data/task1/)
#  * DEV_EN   - the dev.en input file (defaults to data/dev.en)
#  * N        - the number of sentences to convert (defaults to 100)


import errno
import itertools
import os
import subprocess
import sys
import math


def sentence_to_fst(sentence, os = sys.stdout):
    """ Convert a sentence to an equivalent FST in the AT&T FSM format. """

    i = 0
    for latice in sentence:
        (tokens, indices, feature_map) = latice

        for j, w in enumerate(tokens):
            if j == 0:
                os.write("0 {} {} {}\n".format(i + 1, indices[j] + 1, w))
            else:
                if j == len(tokens) - 1:
                    os.write("{} {} {} {} {}\n".format(i, i + 1, indices[j] + 1, w, -math.log(feature_map['prob'])))
                else:
                    os.write("{} {} {} {}\n".format(i, i + 1, indices[j] + 1, w))
            i += 1

        os.write("{}\n".format(i))


def sentence_to_osyms(sentence, os = sys.stdout):
    """ Convert a sentence to a list of output symbols. """

    os.write("<epsilon> 0\n")

    (tokens, indices, feature_map) = sentence[0]

    for i, w in enumerate(tokens):
        os.write("{} {}\n".format(w, indices[i] + 1))


def mkdir_p(path):
    """ Mimick the behaviour of `mkdir -p`. """

    try:
        os.makedirs(path)
    except OSError as e: # Python >2.5
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


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


if __name__ == "__main__":

    # Set the path to the src/, data/ and out/ directories.
    src_dir  = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.realpath(os.getenv('DATA_DIR',
                   os.path.join(os.path.join(src_dir,'..'),'data')))
    out_dir = os.getenv('OUT_DIR', os.path.join(os.path.join(src_dir, '..'), 'out'))
    task5_1_out_dir = os.path.join(out_dir, 'task5.1')

    # Make sure the out/ directory exists.
    mkdir_p(task5_1_out_dir)

    # Set the path to the input file (dev.en).
    dev_en = os.getenv('DEV_EN',os.path.join(data_dir,'dev.enpp.nbest'))

    # Set the number of sentences to convert to FSTs.
    n = os.getenv('N',10)

    # Convert English sentences to FSTs.
    with open(dev_en, 'r') as f:
        sentences = parse_sentences(f)

    for i, sentence in enumerate(sentences):

        if i >= n:
            break

        sys.stdout.write("\r{}/{}".format(i + 1, n))
        sys.stdout.flush()

        fst_txt_file = os.path.join(task5_1_out_dir,'dev.en.{}.fst.txt'.format(i))
        with open(fst_txt_file, 'w') as f: sentence_to_fst(sentence, f)

        osyms_file = os.path.join(task5_1_out_dir,'dev.en.{}.osyms'.format(i))
        with open(osyms_file, 'w') as f: sentence_to_osyms(sentence, f)

        fst_file = os.path.join(task5_1_out_dir,'dev.en.{}.fst'.format(i))
        subprocess.call(['fstcompile',
                         '--keep_osymbols',
                         '--osymbols={}'.format(osyms_file),
                         fst_txt_file,fst_file])

        subprocess.call(['fstpush','--push_weights=true', fst_file, fst_file])
        subprocess.call(['fstdeterminize', fst_file, fst_file])
        subprocess.call(['fstminimize', fst_file, fst_file])

        subprocess.call(['fstarcsort',
                         '--sort_type=olabel',
                         fst_file,fst_file])

        dot_file = os.path.join(task5_1_out_dir, 'dev.en.{}.dot'.format(i))
        subprocess.call(['fstdraw',
                         '--portrait=true',
                         fst_file, dot_file])

        png_file = os.path.join(task5_1_out_dir, 'dev.en.{}.png'.format(i))
        subprocess.call(['dot', '-Tpng', '-Gdpi=300', dot_file, '-o', png_file])

    sys.stdout.write("\r")
    sys.stdout.flush()