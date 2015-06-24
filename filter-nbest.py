#!/usr/bin/env python2

import sys
import gzip

NBEST_DELIM = " ||| "

if __name__ == "__main__":
    try:
        src = sys.argv[1]
        nbest = sys.argv[2]
        lim = int(sys.argv[3])
    except IndexError:
        print "Usage: %s <src phrase file> <nbest file> <max phrase len>\n" % sys.argv[0]
        sys.exit(1)

    # Handle gzipped n-best files
    open_func = open
    new_nbest_file = "%s.%d" % (nbest, lim)
    if nbest.endswith(".gz"):
        open_func = gzip.open
        new_nbest_file = "%s.%d.gz" % (nbest.split(".gz")[0], lim)

    phrases = []
    hypotheses = {}
    n_empty_lines = 0

    # Collect source phrases
    with open(src, "rb") as src_data:
        for line in src_data:
            line = line.rstrip()
            if line:
                phrases.append(line.rstrip() + "\n")
            else:
                phrases.append("")
                n_empty_lines += 1

    n_phrases = len(phrases)
    print "%s: %d phrases (%d empty lines)" % (src, n_phrases, n_empty_lines)

    print "Reading n-best file."
    with open_func(nbest, "rb") as nbest_data:
        for line in nbest_data:
            fields = line.rstrip().split(NBEST_DELIM)
            sent_id = int(fields[0])
            try:
                hypotheses[sent_id].append(fields[1:])
            except KeyError:
                hypotheses[sent_id] = [fields[1:]]

    # 1st pass: Filter out long source phrases and their hypotheses
    print "1st pass from left to right"
    n_removed_srcp = 0
    for i, p in enumerate(phrases):
        l_words = len(p.split())
        if l_words > lim or l_words == 0:
            n_removed_srcp += 1
            phrases[i] = None
            hypotheses[i] = []

    print "Filtered out %d source phrases (%.4f%%)" % (n_removed_srcp,
            100*float(n_removed_srcp) / n_phrases)

    n_removed_srcp = 0

    print "Total source phrases: %d" % len(phrases)

    print "2nd pass from right to left"
    for sent_id, hypos in hypotheses.items():
        if hypos:
            n_removed_hyp = 0
            for i, sent in enumerate(hypos):
                sent_len = len(sent[0].rstrip().split())
                if sent_len > lim:
                    hypos[i] = None
                    n_removed_hyp += 1

            if len(hypos) == n_removed_hyp:
                n_removed_srcp += 1
                # No sentences left for this hyp, remove it
                hypotheses[sent_id] = None
                # Mark corresponding source phrase as None also
                phrases[sent_id] = None

    print "Filtered out %d further source phrases" % n_removed_srcp

    # These should be equal
    final_phrases = [p for p in phrases if p]
    assert(len(final_phrases) == len([h for h in hypotheses.keys() if hypotheses[h]]))

    # Dump files
    f_src = open("%s.%d" % (src, lim), "wb")
    f_src.writelines(final_phrases)
    f_src.close()

    del final_phrases, phrases

    line_ctr = 0

    f_out = open_func(new_nbest_file, "wb")
    print "Dumping nbest file.."
    for sent_id in sorted(hypotheses.keys()):
        h = hypotheses[sent_id]
        if h:
            nbest_lines = []
            for s in [x for x in h if x]:
                s.insert(0, str(line_ctr))
                nbest_lines.append(NBEST_DELIM.join(s) + "\n")
            line_ctr += 1
            f_out.writelines(nbest_lines)

    f_out.close()
