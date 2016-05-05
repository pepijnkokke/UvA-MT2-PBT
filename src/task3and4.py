#!/usr/bin/env python
#
#

from task1 import mkdir_p


import itertools
import math
import os
import subprocess
import sys
import operator


def find_best_derivations(print_data):
    all_arcs = [x.split('\t') for x in print_data.split('\n')]
    starting_state = '0'

    results = find_best_derivations_rec(all_arcs, starting_state)
    sorted_results = sorted(results, key=lambda tup: tup[1])

    return sorted_results


def find_best_derivations_rec(all_arcs, state):
    finishing_state = '1'

    current_arcs = [x for x in all_arcs if x[0] == state]

    results = []

    for arc in current_arcs:

        t = arc[1]
        e = arc[2]
        j = arc[3]

        if len(arc) >= 5:
            p = float(arc[4])
        else:
            p = 0.0

        if t == finishing_state:
            return [([j], [e], p)]
        else:
            old_results = find_best_derivations_rec(all_arcs, t)
            for (js, es, ps) in old_results:
                results.append(([j] + js, [e] + es, ps + p))

    return results


def best_derivations_alignments(print_result, os = sys.stdout):
    for (js, es, p) in find_best_derivations(print_result):

        constructing_phrase = False
        finished_english_phrase = False
        phrase = []
        phrase_begin = 0
        phrase_end = 0

        for i,j in enumerate(js):

            e = int(es[i])

            if constructing_phrase:
                if j == '<epsilon>' and finished_english_phrase == False:
                    phrase_end = e
                    continue
                else:
                    finished_english_phrase = True
                    if e == 0:
                        phrase.append(j)
                        continue
                    else:
                        os.write("{} |{}-{}| ".format(' '.join(phrase), phrase_begin, phrase_end))
                        phrase = []
                        constructing_phrase = False
                        finished_english_phrase = False

            if j == '<epsilon>':
                constructing_phrase = True
                phrase_begin = e
                phrase_end = e
            else:
                os.write("{} |{}-{}| ".format(j, e, e))

        if constructing_phrase:
            os.write("{} |{}-{}| ".format(' '.join(phrase), phrase_begin, phrase_end))

        os.write("\n")


def find_best_derivation(print_result):
    (js, _, _) = find_best_derivations(print_result)[0];
    return ' '.join([x for x in js if x != '<epsilon>'])


def find_best_translation(print_result):

    score_map = {}

    for (js, _, p) in find_best_derivations(print_result):

        j = ' '.join([x for x in js if x != '<epsilon>'])

        if j in score_map:
            score_map[j] += p
        else:
            score_map[j] = p

    score_items = score_map.items()
    (translation, _) = sorted(score_items, key=operator.itemgetter(1))[0]

    return translation


if __name__ == "__main__":

    # Set the path to the src/, data/ and out/ directories.
    src_dir  = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.getenv('DATA_DIR',os.path.join(os.path.join(src_dir,'..'),'data'))
    out_dir = os.getenv('OUT_DIR', os.path.join(os.path.join(src_dir, '..'), 'out'))

    task1_out_dir = os.path.join(out_dir, 'task1')
    task2_out_dir = os.path.join(out_dir, 'task2')
    task3_out_dir = os.path.join(out_dir, 'task3')
    task4_out_dir = os.path.join(out_dir, 'task4')

    # Make sure the out/ directory exists.
    mkdir_p(task3_out_dir)
    mkdir_p(task4_out_dir)

    # Set the path to the input file (dev.en).
    dev_en_fst\
        = os.path.join(task1_out_dir,'dev.en')
    grammar_fst            = os.path.join(task1_out_dir,'grammar')

    best_derivations = []
    best_translations = []

    # Set the number of sentences to convert to FSTs.
    s = os.getenv('S', 0)
    n = os.getenv('N', 1416)

    # Iterate over fsts
    for i in range(0, n):

        sys.stdout.write("\r{}/{}".format(i + 1, n))
        sys.stdout.flush()

        j = s + i

        dev_en_file = os.path.join(task1_out_dir,'dev.en.{}.fst'.format(j))
        grammar_file = os.path.join(task2_out_dir,'grammar.{}.fst'.format(j))

        composed_file = os.path.join(task3_out_dir, 'composed.{}.fst'.format(j))
        subprocess.call(['fstcompose',
                         '--connect=false',
                         dev_en_file, grammar_file, composed_file])

        isyms_file = os.path.join(task1_out_dir, 'dev.en.{}.osyms'.format(j))

        shortest_file = os.path.join(task3_out_dir, 'shortest.{}.fst'.format(j))
        subprocess.call(['fstshortestpath',
                         '--nshortest=100',
                         composed_file, shortest_file])

        # subprocess.call(['fstrmepsilon', shortest_file, shortest_file])
        # subprocess.call(['fstdisambiguate', shortest_file, shortest_file])
        subprocess.call(['fstrmepsilon', shortest_file, shortest_file])
        subprocess.call(['fstpush', '--push_weights=true', shortest_file, shortest_file])

        print_result = subprocess.check_output(['fstprint', shortest_file])

        best_file = os.path.join(task3_out_dir, 'monotone.100best.{}'.format(j))
        with open(best_file, 'w') as f:
            best_derivations_alignments(print_result, f)

        best_derivations.append(find_best_derivation(print_result))
        best_translations.append(find_best_translation(print_result))

        # dot_file = os.path.join(task3_out_dir, 'shortest.{}.dot'.format(j))
        # subprocess.call(['fstdraw',
        #                  '--portrait=true',
        #                  shortest_file, dot_file])
        #
        # png_file = os.path.join(task3_out_dir, 'shortest.{}.png'.format(j))
        # subprocess.call(['dot', '-Tpng','-Gdpi=300', dot_file, '-o', png_file])

    sys.stdout.write("\r")
    sys.stdout.flush()

    best_derivations_file = os.path.join(task4_out_dir, 'monotone.der')
    with open(best_derivations_file, 'w') as f:
        for d in best_derivations:
            f.write('{}\n'.format(d))

    best_translations_file = os.path.join(task4_out_dir, 'monotone.trans')
    with open(best_translations_file, 'w') as f:
        for t in best_translations:
            f.write('{}\n'.format(t))
