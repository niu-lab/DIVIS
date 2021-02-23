#!/usr/bin python3
import sys
import re


#def extract_insertsizse(filename):
#    restr = r"MEDIAN_INSERT_SIZE"
#    pattern = re.compile(restr)
#    found = False
#    with open(filename, "r") as file:
#        while True:
#            line = file.readline()
#            if found:
#                insert_size = re.split(r"\s", line)[0]
#                break
#            if re.match(pattern, line):
#                found = True
#    return insert_size


def generate_pindel_config(normal_bam, tumor_bam, output_file):
    normal_insert_size = 500
    tumor_insert_size = 500
    tpl = '''{normal_bam}\t{normal_size}\tNORMAL
{tumor_bam}\t{tumor_size}\tTUMOR'''.format(normal_bam=normal_bam,
                                           tumor_bam=tumor_bam,
                                           normal_size=normal_insert_size,
                                           tumor_size=tumor_insert_size)

    with open(output_file, "w+") as out:
        out.write(tpl)


if __name__ == "__main__":
    generate_pindel_config(sys.argv[1], sys.argv[2], sys.argv[3])
