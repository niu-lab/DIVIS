#!/usr/env python3
import sys
import os


def generate_filter_config(input,
                           pindel2vcf,
                           ref,
                           refdate,
                           mode,
                           heterozyg_min_var_allele_freq,
                           homozyg_min_var_allele_freq,
                           apply_filter,
                           min_coverages,
                           min_var_allele_freq,
                           require_balanced_reads,
                           remove_complex_indels,
                           max_num_homopolymer_repeat_units,
                           config_out):
    input = os.path.abspath(input)
    tpl = '''pindel.filter.pindel2vcf = {pindel2vcf}
pindel.filter.variants_file = {input}
pindel.filter.REF = {ref}
pindel.filter.date = {refdate}
pindel.filter.mode = {mode}
pindel.filter.heterozyg_min_var_allele_freq = {heterozyg_min_var_allele_freq}
pindel.filter.homozyg_min_var_allele_freq = {homozyg_min_var_allele_freq}
pindel.filter.apply_filter = {apply_filter}
pindel.filter.germline.min_coverages = {min_coverages}
pindel.filter.germline.min_var_allele_freq = {min_var_allele_freq}
pindel.filter.germline.require_balanced_reads = {require_balanced_reads}
pindel.filter.germline.remove_complex_indels = {remove_complex_indels}
pindel.filter.germline.max_num_homopolymer_repeat_units = {max_num_homopolymer_repeat_units}
'''.format(pindel2vcf=pindel2vcf,
           input=input,
           ref=ref,
           refdate=refdate,
           mode=mode,
           heterozyg_min_var_allele_freq=heterozyg_min_var_allele_freq,
           homozyg_min_var_allele_freq=homozyg_min_var_allele_freq,
           apply_filter=apply_filter,
           min_coverages=min_coverages,
           min_var_allele_freq=min_var_allele_freq,
           require_balanced_reads=require_balanced_reads,
           remove_complex_indels=remove_complex_indels,
           max_num_homopolymer_repeat_units=max_num_homopolymer_repeat_units
           )

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
                           sys.argv[10],
                           sys.argv[11],
                           sys.argv[12],
                           sys.argv[13],
                           sys.argv[14],
                           )
