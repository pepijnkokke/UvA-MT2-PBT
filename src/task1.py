#!/usr/bin/env python
#
# Convert the first 100 sentence in data/dev.en to FSTs.

import errno
import itertools
import os
import sys


def sentence_to_fst(sentence, os = sys.stdout):
    """ Convert a sentence to an equivalent FST in the AT&T FSM format. """

    state      = 0
    words      = sentence.split()
    last_index = len(words) - 1

    for i, w in enumerate(words):
        os.write("{} {} {} {}\n".format(i, i + 1, i + 1, w))

    os.write("{}\n".format(i + 1))


def sentence_to_osyms(sentence, os = sys.stdout):
    """ Convert a sentence to a list of output symbols. """

    state = 0
    words = sentence.split()

    os.write("<eps> 0\n")

    for i, w in enumerate(words):
        os.write("{} {}\n".format(w, i + 1))


def mkdir_p(path):
    """ Mimick the behaviour of `mkdir -p`. """

    try:
        os.makedirs(path)
    except OSError as e: # Python >2.5
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


if __name__ == "__main__":

    # Set the path to the src/, data/ and out/ directories.
    src_dir  = os.getenv('SRC_DIR',os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.getenv('DATA_DIR',os.path.join(os.path.join(src_dir,'..'),'data'))
    out_dir  = os.getenv('OUT_DIR',os.path.join(data_dir,'task1'))

    # Make sure the out/ directory exists.
    mkdir_p(out_dir)

    # Set the path to the input file (dev.en).
    dev_en   = os.getenv('DEV_EN',os.path.join(data_dir,'dev.en'))

    # Set the number of sentences to convert to FSTs.
    n        = os.getenv('N',100)

    with open(dev_en, 'r') as f:
        sentences = list(itertools.islice(f, n))

    for i, sentence in enumerate(sentences):

        sys.stdout.write("\r{}/{}".format(i + 1, n))
        sys.stdout.flush()

        fst_file = os.path.join(out_dir,'dev.en.{}.fst'.format(i))
        with open(fst_file, 'w') as f: sentence_to_fst(sentence, f)

        osyms_file = os.path.join(out_dir,'dev.en.{}.osyms'.format(i))
        with open(osyms_file, 'w') as f: sentence_to_osyms(sentence, f)

    sys.stdout.write("\r")
    sys.stdout.flush()
