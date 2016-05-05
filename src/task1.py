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


def sentence_to_fst(sentence, os = sys.stdout):
    """ Convert a sentence to an equivalent FST in the AT&T FSM format. """

    state      = 0
    words      = sentence.split()
    last_index = len(words) - 1

    for i, w in enumerate(words):
        os.write("{} {} {} {}\n".format(i, i + 1, i + 1, w))

    os.write("{}\n".format(i + 1))


def sentence_to_isyms(sentence, os = sys.stdout):
    """ Convert a sentence to a list of input symbols. """

    state = 0
    words = sentence.split()

    os.write("0 <epsilon>\n")

    for i, w in enumerate(words):
        os.write("{} {}\n".format(i + 1, w))


def sentence_to_osyms(sentence, os = sys.stdout):
    """ Convert a sentence to a list of output symbols. """

    state = 0
    words = sentence.split()

    os.write("<epsilon> 0\n")

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
    src_dir  = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.realpath(os.getenv('DATA_DIR',
                   os.path.join(os.path.join(src_dir,'..'),'data')))
    out_dir = os.getenv('OUT_DIR', os.path.join(os.path.join(src_dir, '..'), 'out'))
    task1_out_dir = os.path.join(out_dir, 'task1')

    # Make sure the out/ directory exists.
    mkdir_p(task1_out_dir)

    # Set the path to the input file (dev.en).
    dev_en = os.getenv('DEV_EN',os.path.join(data_dir,'dev.en'))

    # Set the number of sentences to convert to FSTs.
    s = os.getenv('S', 0)
    n = os.getenv('N', 1416)

    # Convert English sentences to FSTs.
    with open(dev_en, 'r') as f:
        sentences = list(itertools.islice(f, s, s + n))

    for i, sentence in enumerate(sentences):

        sys.stdout.write("\r{}/{}".format(i + 1, n))
        sys.stdout.flush()

        j = s + i

        fst_txt_file = os.path.join(task1_out_dir,'dev.en.{}.fst.txt'.format(j))
        with open(fst_txt_file, 'w') as f: sentence_to_fst(sentence, f)

        osyms_file = os.path.join(task1_out_dir,'dev.en.{}.osyms'.format(j))
        with open(osyms_file, 'w') as f: sentence_to_osyms(sentence, f)

        fst_file = os.path.join(task1_out_dir,'dev.en.{}.fst'.format(j))
        subprocess.call(['fstcompile',
                         '--keep_osymbols',
                         '--osymbols={}'.format(osyms_file),
                         fst_txt_file, fst_file])

        subprocess.call(['fstarcsort',
                         '--sort_type=olabel',
                         fst_file, fst_file])

        # dot_file = os.path.join(task1_out_dir, 'dev.en.{}.dot'.format(j))
        # subprocess.call(['fstdraw',
        #                  '--portrait=true',
        #                  fst_file, dot_file])
        #
        # png_file = os.path.join(task1_out_dir, 'dev.en.{}.png'.format(j))
        # subprocess.call(['dot', '-Tpng', '-Gdpi=300', dot_file, '-o', png_file])

    sys.stdout.write("\r")
    sys.stdout.flush()
