'''
Renames paired end reads so that they can be recognized by the FASTQ de-interlacer tool in Galaxy.
Input: one fastq file with paired end reads named according to the following convention:
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
@some_identifier.another_identifier.1 the rest of the name/1
@some_identifier.another_identifier.2 the rest of the name/2
(same operation done for quality scores headers)
'''

import sys

def rename_read(num, line):
    if num % 4 == 0:
        if line.split('.')[2].split(' ')[0] == '1':
            new_line = line.replace('\n', '/1\n')
            return new_line
        elif line.split('.')[2].split(' ')[0] == '2':
            new_line = line.replace('\n', '/2\n')
            return new_line
        else:
            print("Wrong sequence header format. Read number not found.")
            print(line)
    elif num % 4 == 2:
        if line.split('.')[2].split(' ')[0] == '1':
            new_line = line.replace('\n', '/1\n')
            return new_line
        elif line.split('.')[2].split(' ')[0] == '2':
            new_line = line.replace('\n', '/2\n')
            return new_line
        else:
            print("Wrong quality header format. Read number not found.")
            print(line)
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
    