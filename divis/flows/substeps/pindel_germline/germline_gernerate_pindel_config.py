#!/usr/bin python3
import sys
import re


def extract_insertsizse(filename):
    restr = r"MEDIAN_INSERT_SIZE"
    pattern = re.compile(restr)
    found = False
    with open(filename, "r") as file:
        while True:
            line = file.readline()
            if found:
                insert_size = re.split(r"\s", line)[0]
                break
            if re.match(pattern, line):
                found = True
    return insert_size


def generate_pindel_config(bam_file, insertsize_file, sample_name, output_file):
    insert_size = extract_insertsizse(insertsize_file)
    tpl = '''{bam_file}\t{insert_size}\t{sample_name}
'''.format(bam_file=bam_file,
           insert_size=insert_size,
           sample_name=sample_name)

    with open(output_file, "w+") as out:
        out.write(tpl)


if __name__ == "__main__":
    generate_pindel_config(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
