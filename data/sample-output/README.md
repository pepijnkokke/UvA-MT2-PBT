# Sample output

I have performed monotone translation of the last 100 sentences in the dev set as well as lattice translation.
Here you will find the translations my system produced: I used a max-derivation decision rule (but I am not showing the alignments in the output).

* Reference: dev-tail100.ja
* Monotone translation: dev-tail100.monotone 
* Lattice translation: dev-tail100.lattice

These are the BLEU scores I get:

    perl ../multi-bleu.perl dev-tail100.ja < dev-tail100.monotone
    BLEU = 14.14, 54.6/22.2/9.0/3.6 (BP=1.000, ratio=1.077, hyp_len=2941, ref_len=2731)
    
    perl ../multi-bleu.perl dev-tail100.ja < dev-tail100.lattice
    BLEU = 18.42, 58.8/27.4/12.5/6.2 (BP=0.981, ratio=0.981, hyp_len=2680, ref_len=2731)


My BLEU scores on the first 100 sentences was around 13 (monotone) and 20 (lattice).
