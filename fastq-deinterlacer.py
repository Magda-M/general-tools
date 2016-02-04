'''
Generate separate fastq files for forward and reverse reads if the input file contains both.
Assumptions:
- reads are sorted,
- all pairs are complete,
- input file has a fastq extension.
'''
import sys

def deinterlace(fastq, r1, r2):
    with open(fastq) as f:
        with open(r1, 'w') as forw, open(r2, 'w') as rev:
            [forw.write(line) if (i % 8 < 4) else rev.write(line) for i, line in enumerate(f)]
            
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python %s input_fastq" % sys.argv[0])
        sys.exit(1)
    input_fastq = sys.argv[1]
    if input_fastq.split('.')[-1] != 'fastq':
        print("Input file must have 'fastq' extension")
        sys.exit(1)        
    out_r1 = input_fastq.replace('.fastq', '_R1.fastq')
    out_r2 = input_fastq.replace('.fastq', '_R2.fastq')
    deinterlace(input_fastq, out_r1, out_r2)
    print("Done. Output written to: %s and %s" % (out_r1, out_r2))