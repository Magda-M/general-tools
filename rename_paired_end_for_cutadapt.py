'''
Renames paired end reads so that they can be processed by cutadapt in paired-end mode.
Input: fastq file with paired end reads named according to the following convention:
@some_identifier.another_identifier.1 the rest of the name
ACGTA
+some_identifier.another_identifier.1 the rest of the name
8?@DD
@some_identifier.another_identifier.2 the rest of the name
CCGAA
+some_identifier.another_identifier.2 the rest of the name
8?@DD
(the read number in pair is after the 2nd dot and before the 1st space)
Output:
@some_identifier.another_identifier the rest of the name/1
@some_identifier.another_identifier the rest of the name/2
(same operation done for quality scores headers)
'''

import sys

def rename_read(num, line):
    if num % 4 == 0 or num % 4 == 2:
       new_line = '.'.join(line.split(' ')[0].split('.')[:2]) + ' ' + ' '.join(line.split(' ')[1:])
       return new_line
    else:
        return line
          
def run(fastq, new_fastq):
    with open(fastq) as f1:
        with open(new_fastq, 'w') as f2:
            for i, line in enumerate(f1):
                if len(line.strip()) > 0:
                    new_line = rename_read(i, line)
                    f2.write(new_line)
                
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python %s input_fastq output_fastq" % sys.argv[0])
        sys.exit(1)
    input_fastq = sys.argv[1]
    output_fastq = sys.argv[2]
    run(input_fastq, output_fastq)
    print("Done.")
    