#!/usr/env python3
import sys


def generate_filter_config(input, vaf, cov, hom, pindel2vcf, ref, refname, refdate, output, config_out):
    tpl = '''indel.filter.input = {input}
indel.filter.vaf = {vaf}
indel.filter.cov = {cov}
indel.filter.hom = {hom}
indel.filter.pindel2vcf = {pindel2vcf}
indel.filter.reference = {ref}
indel.filter.referencename = {refname}
indel.filter.referencedate = {refdate}
indel.filter.output = {output}
'''.format(input=input,
           vaf=vaf,
           cov=cov,
           hom=hom,
           pindel2vcf=pindel2vcf,
           ref=ref,
           refname=refname,
           refdate=refdate,
           output=output)

    with open(config_out, "w+") as out:
        out.write(tpl)


if __name__ == "__main__":
    if len(sys.argv) < 9:
        print("too less args")
        exit(1)
    generate_filter_config(sys.argv[1],
                           sys.argv[2],
                           sys.argv[3],
                           sys.argv[4],
                           sys.argv[5],
                           sys.argv[6],
                           sys.argv[7],
                           sys.argv[8],
                           sys.argv[9],
                           sys.argv[10],)
