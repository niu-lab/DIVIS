#!/usr/env/bin python3
import os
import sys
from divis.macros import read_macros, write_macros
from divis.utils import dir_create

substeps_macros_map = {
    "normal_align": "align",
    "tumor_align": "align",
    "varscan_somatic": "varscan_somatic",
    "strelka_somatic": "strelka_somatic",
    "pindel_somatic": "pindel_somatic",
    "vardict_somatic": "vardict_somatic",
}

substep_macros_dir = os.path.join(os.curdir, "tpl")


def extract_macros(tpl_macros, all_macros):
    for macro in tpl_macros:
        tpl_macros[macro] = all_macros[macro] if macro in all_macros else tpl_macros[macro]
    return tpl_macros


def process(defined_macro_file):
    required_macros = read_macros(defined_macro_file)
    gen_config_dir = os.path.join(os.curdir, "config_dir")
    dir_create(gen_config_dir)

    # specific
    normal_bam = os.path.join(os.path.curdir,
                              "divis.normal.align.out/align/{}.normal.bam".format(required_macros.get("SAMPLE_NAME")))
    tumor_bam = os.path.join(os.path.curdir,
                             "divis.tumor.align.out/align/{}.tumor.bam".format(required_macros.get("SAMPLE_NAME")))

    required_macros["NORMAL_BAM"] = os.path.abspath(normal_bam)
    required_macros["TUMOR_BAM"] = os.path.abspath(tumor_bam)

    # read user define macros
    macros = dict()
    for substep in substeps_macros_map:
        macro = read_macros(os.path.join(substep_macros_dir, "{}.macros".format(substeps_macros_map[substep])))
        substep_macro = extract_macros(macro, required_macros)
        macros[substep] = substep_macro

    # change special macros
    macros["normal_align"]["SAMPLE_NAME"] = "{}.normal".format(required_macros.get("SAMPLE_NAME"))
    macros["normal_align"]["R1"] = required_macros.get("NORMAL_R1")
    macros["normal_align"]["R2"] = required_macros.get("NORMAL_R2")
    macros["normal_align"][
        "RG"] = "\'@RG\\tID:{normal_barcode}\\tSM:{normal_barcode}_N\\tLB:{normal_barcode}\\tPL:{platform}\'".format(
        normal_barcode=required_macros.get("NORMAL_BARCODE"),
        platform=required_macros.get("PLATFORM")
    )
    macros["tumor_align"]["SAMPLE_NAME"] = "{}.tumor".format(required_macros.get("SAMPLE_NAME"))
    macros["tumor_align"]["R1"] = required_macros.get("TUMOR_R1")
    macros["tumor_align"]["R2"] = required_macros.get("TUMOR_R2")
    macros["tumor_align"][
        "RG"] = "\'@RG\\tID:{tumor_barcode}\\tSM:{tumor_barcode}\\tLB:{tumor_barcode}\\tPL:{platform}\'".format(
        tumor_barcode=required_macros.get("TUMOR_BARCODE"),
        platform=required_macros.get("PLATFORM")
    )

    # write to file
    for name in macros:
        write_macros(macros.get(name), os.path.join(gen_config_dir, "{}.macros".format(name)))


if __name__ == '__main__':
    defined_macro_file = os.path.join(os.curdir, "required.macros")
    process(defined_macro_file)
