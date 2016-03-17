"""
SOURCE: https://gist.github.com/brentp/6625544
split a single fastq file in to random, non-overlapping subsets
arguments:
+ fastq file
+ number of splits
+ number of reps

e.g.:

    python fq.split.py input.fastq 3 4

will create 12 new files in 4 sets of 3. Each
set of 3 will contain all of the original records.
"""

import gzip
import random
from itertools import islice, izip

xopen = lambda fq: gzip.open(fq) if fq.endswith('.gz') else open(fq)


def fqiter(fq, lines_per_read):
    with xopen(fq) as fh:
        fqclean = (x.strip("\r\n") for x in fh if x.strip())
        while True:
            rec = [x for x in islice(fqclean, lines_per_read)]
            if not rec: raise StopIteration
            assert all(rec) and len(rec) == lines_per_read
            yield rec

def fqsplit(fq, nchunks, nreps, paired, prefix=None):
    if paired:
        lines_per_read = 8
    else:
        lines_per_read = 4
    if prefix == None: prefix = fq + ".split"
    prefix += "chunk-%i.rep-%i.fq"

    fq_size = sum(1 for x in xopen(fq) if len(x.strip("\r\n"))>0)
    assert fq_size % lines_per_read == 0
    fq_size /= lines_per_read # number of records
    print >>sys.stderr, "num reads/read pairs:", fq_size
    print >>sys.stderr, "num chunks to split into:", nchunks
    
    if fq_size % nchunks == 0 :
        chunk_size = fq_size // nchunks
    else:
        chunk_size = 1 + (fq_size) // nchunks
    print >>sys.stderr, "chunk_size:", chunk_size

    for rep in range(1, nreps + 1):

        files = [open(prefix % (c, rep), 'w') for c in range(1, nchunks + 1)]
        ints = range(fq_size)
        random.shuffle(ints)

        for i, fqr in izip(ints, fqiter(fq, lines_per_read)):
            chunk, chunk_i = divmod(i, chunk_size)
            print >>files[chunk], "\n".join(fqr)
        [f.close() for f in files]

if __name__ == "__main__":

    import sys

    fq = sys.argv[1]
    nchunks = int(sys.argv[2])
    nreps = int(sys.argv[3])
    paired = bool(int(sys.argv[4]))
    print paired# 0 = single, 1 = paired end reads
    fqsplit(fq, nchunks, nreps, paired)