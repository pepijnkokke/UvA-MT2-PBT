#!/usr/bin/env python
#
#

from task1 import mkdir_p


import itertools
import math
import os
import subprocess
import sys


if __name__ == "__main__":

    # Set the path to the src/, data/ and out/ directories.
    src_dir  = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.getenv('DATA_DIR',os.path.join(os.path.join(src_dir,'..'),'data'))
    out_dir = os.getenv('OUT_DIR', os.path.join(os.path.join(src_dir, '..'), 'out'))

    task1_out_dir = os.path.join(out_dir, 'task1')
    task2_out_dir = os.path.join(out_dir, 'task2')
    task3_out_dir = os.path.join(out_dir, 'task3')

    # Make sure the out/ directory exists.
    mkdir_p(task3_out_dir)

    # Set the path to the input file (dev.en).
    dev_en_fst\
        = os.path.join(task1_out_dir,'dev.en')
    grammar_fst            = os.path.join(task1_out_dir,'grammar')

    # Set the number of sentences to convert to FSTs.
    n = os.getenv('N',10)

    # Iterate over fsts
    for i in range(0,n):

        sys.stdout.write("\r{}/{}".format(i + 1, n))
        sys.stdout.flush()

        dev_en_file = os.path.join(task1_out_dir,'dev.en.{}.fst'.format(i))
        grammar_file = os.path.join(task2_out_dir,'grammar.{}.fst'.format(i))

        composed_file = os.path.join(task3_out_dir, 'composed.{}.fst'.format(i))
        subprocess.call(['fstcompose',
                         '--connect=false',
                         dev_en_file, grammar_file, composed_file])

        isyms_file = os.path.join(task1_out_dir, 'dev.en.{}.osyms'.format(i))

        shortest_file = os.path.join(task3_out_dir, 'shortest.{}.fst'.format(i))
        subprocess.call(['fstshortestpath',
                         '--nshortest=10',
                         composed_file, shortest_file ])

        dot_file = os.path.join(task3_out_dir, 'shortest.{}.dot'.format(i))
        subprocess.call(['fstdraw',
                         '--portrait=true',
                         shortest_file, dot_file])

        png_file = os.path.join(task3_out_dir, 'shortest.{}.png'.format(i))
        subprocess.call(['dot', '-Tpng','-Gdpi=300', dot_file, '-o', png_file])


    sys.stdout.write("\r")
    sys.stdout.flush()
