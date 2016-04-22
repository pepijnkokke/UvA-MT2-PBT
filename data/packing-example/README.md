# Packing permutations

This is an example for the first sentence in dev.enpp.nbest.
My approach was to create a trivial lattice with all permutations. The last arc of each permutation carries the "cost" of the permutation, that is, -ln(prob(permutation)). I used a "negative log" semantics because that's the default weight type in OpenFST.
Once that lattice was done, I compiled it and optimised its topology with operations:
1. determinize
2. push
3. minimize
4. topsort

There are other strategies that would work just as well.

I am attaching some of my intermediate files:

* input symbol table: dev.0.isyms.txt
* output symbol table: dev.0.osyms.txt
* FST (text format): dev.0.fst.txt
* FST (binary -- see below): dev.0.fst.bin
* FST illustration (dot format -- see below): dev.0.fst.dot
* FST illustration (in pdf -- see below): dev.0.fst.pdf
* Optimised FST (txt): dev.0.fst-det-push-min-tsort.txt
* Optimised FST (binary): dev.0.fst-det-push-min-tsort.bin
* Optimised FST (dot): dev.0.fst-det-push-min-tsort.dot
* Optimised FST (pdf): dev.0.fst-det-push-min-tsort.pdf


# Binarizing FSTs

    fstcompile --isymbols=dev.0.isyms.txt --keep_isymbols --osymbols=dev.0.osyms.txt --keep_osymbols dev.0.fst.txt dev.0.fst.bin

# Drawing FSTs

    fstdraw --isymbols=dev.0.isyms.txt --osymbols=dev.0.osyms.txt dev.0.fst.bin dev.0.fst.dot
    dot -Tpdf dev.0.fst.dot > dev.0.fst.pdf
