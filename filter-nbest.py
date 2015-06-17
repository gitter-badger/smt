#!/usr/bin/env python2

import sys
import gzip

if __name__ == "__main__":
    try:
        src = sys.argv[1]
        nbest = sys.argv[2]
        lim = int(sys.argv[3])
    except IndexError:
        print "Usage: %s <src phrase file> <nbest file> <max phrase len>\n" % sys.argv[0]
        sys.exit(1)

    keep_lines = []
    new_lines = []
    # First select line numbers with length <= lim
    with open(src, "rb") as src_data:
        for ctr, line in enumerate(src_data.readlines()):
            # It's possible to have empty lines in src phrases..
            if line[0] != '\n' and len(line.split(" ")) <= lim:
                keep_lines.append(ctr)
                new_lines.append(line)

    f = open("%s.%d" % (src, lim), "wb")
    f.writelines(new_lines)
    f.close()

    open_func = open
    new_nbest_file = "%s.%d" % (nbest, lim)
    if nbest.endswith(".gz"):
        open_func = gzip.open
        new_nbest_file = "%s.%d.gz" % (nbest.split(".gz")[0], lim)

    hyp_start_id = None

    new_nbest = []

    # Then process the n-best file to eliminate hypotheses
    # with source phrases > lim
    # Discard also translations with phrases > lim
    with open_func(nbest, "rb") as nbest_data:
        for line in nbest_data:
            fields = line.rstrip().split(" ||| ")
            if int(fields[0]) in keep_lines:
                # It's possible that the translation is bigger than the limit
                phr_len = len(fields[1].rstrip().split(" "))
                if phr_len <= lim:
                    new_nbest.append(line)

    f_out = open_func(new_nbest_file, "wb")
    f_out.writelines(new_nbest)
    f_out.close()
