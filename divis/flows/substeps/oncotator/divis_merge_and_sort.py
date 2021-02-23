#!/usr/bin/env python3

import re
import os
import collections
from sys import stdout, stderr
import click
from GPyFlow.proc import run_cmd

MAFLITE_HEADER = "chr\tstart\tend\tref_allele\talt_allele"
MAFLITE_HEADER_PATTERN = r'.*ref_allele.*'
MAFLITE_HEADER_RE = re.compile(MAFLITE_HEADER_PATTERN)


def merge(vcfs, name):
    merged_maflite = "{}.merged.maflite".format(name)
    maflites = list()
    for vcf in vcfs:
        if len(vcf.strip()) == 0:
            continue
        if not os.path.exists(vcf):
            stderr.write("ERROR:not find {}\n".format(vcf))
            exit(1)

        maflite_filename = "{}.maflite".format(os.path.basename(vcf))
        cmd = "perl ./divis_anno_vcf_with_oncotator.pl {vcf} {maflite}".format(vcf=vcf,
                                                                             maflite=maflite_filename)
        run_cmd(cmd, stdout, stderr)
        maflites.append(maflite_filename)

    merged_file = open(merged_maflite, 'w+')
    merged_file.write(MAFLITE_HEADER + os.linesep)
    for maflite in maflites:
        with open(maflite, 'r') as file:
            for line in file:
                if MAFLITE_HEADER_RE.match(line):
                    continue
                merged_file.write(line)

    merged_file.close()

    return merged_maflite


def transform_no(no):
    if no in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        return "0" + no
    elif no == "X":
        return "24"
    elif no == "Y":
        return "25"
    else:
        return no


def sort(maflite_filepath, name):
    sorted_maflite = "{}.sorted.maflite".format(name)
    sorted_file = open(sorted_maflite, 'w+')
    sorted_file.write(MAFLITE_HEADER + os.linesep)
    lines = dict()
    with open(maflite_filepath, "r") as file:
        for line in file:
            if MAFLITE_HEADER_RE.match(line):
                continue
            splits = line.strip().split("\t")
            chr = splits[0]
            if chr.find("chr") >= 0:
                no = chr[3:]
            else:
                no = chr
            start = splits[1]
            key = "{0}_{1}".format("chr_" + transform_no(no), start)
            if lines.get(key):
                print("key:{0},new line:{1} / already line:{2}".format(key, line.strip(), lines.get(key).strip()))
            lines[key] = line

    ordered_lines = collections.OrderedDict(sorted(lines.items()))
    for key, line in ordered_lines.items():
        sorted_file.write(line)

    sorted_file.close()


def process(vcfs, name):
    sort(merge(vcfs, name), name)


@click.command()
@click.option('--vcfs', required=True, help="VCF Files", type=str)
@click.option('--sample_name', required=True, help="Sample Name", type=str)
def get_maflites(vcfs, sample_name):
    vcf_files = re.split(r"\s+", vcfs)
    process(vcf_files, sample_name)
    pass


if __name__ == "__main__":
    get_maflites()
