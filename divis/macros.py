import os
import re
from divis.config import BASE_DIR

DEFAULT_MACROS_ROOT = os.path.join(BASE_DIR, "macros/default")

DEFAULT_SUBSTEP_MACROS_ROOT = os.path.join(DEFAULT_MACROS_ROOT, "substeps")

DEFAULT_PIPELINE_MACROS_ROOT = os.path.join(DEFAULT_MACROS_ROOT, "pipelines")

DEFAULT_SUBSTEP_MACROS_DICT = {
    "qc": os.path.join(DEFAULT_SUBSTEP_MACROS_ROOT, "qc.macros"),
    "qc_to_align": os.path.join(DEFAULT_SUBSTEP_MACROS_ROOT, "qc_to_align.macros"),
    "align": os.path.join(DEFAULT_SUBSTEP_MACROS_ROOT, "align.macros"),
    "varscan_somatic": os.path.join(DEFAULT_SUBSTEP_MACROS_ROOT, "varscan_somatic.macros"),
    "strelka_somatic": os.path.join(DEFAULT_SUBSTEP_MACROS_ROOT, "strelka_somatic.macros"),
    "pindel_somatic": os.path.join(DEFAULT_SUBSTEP_MACROS_ROOT, "pindel_somatic.macros"),
    "vardict_somatic": os.path.join(DEFAULT_SUBSTEP_MACROS_ROOT, "vardict_somatic.macros"),
    "gatk4_haplotypecaller-germline": os.path.join(DEFAULT_SUBSTEP_MACROS_ROOT,
                                                   "gatk4_haplotypecaller_germline.macros"),
    "oncotator": os.path.join(DEFAULT_SUBSTEP_MACROS_ROOT, "oncotator.macros"),
    "mutect1_somatic":os.path.join(DEFAULT_SUBSTEP_MACROS_ROOT, "mutect1_somatic.macros"),
    "vep":os.path.join(DEFAULT_SUBSTEP_MACROS_ROOT, "vep.macros"),
    "divis_report":os.path.join(DEFAULT_SUBSTEP_MACROS_ROOT,"divis_report.macros")
}

DEFAULT_PIPELINE_MACROS_DICT = {
    "wes_somatic": os.path.join(DEFAULT_PIPELINE_MACROS_ROOT, "wes_somatic.macros"),
}


def read_macros(filename):
    pattern = r'([A-Z0-9_]+)=(.*)\n'
    macros_re = re.compile(pattern)
    macros_dict = dict()
    with open(filename, "r") as file:
        for line in file:
            matched = macros_re.match(line)
            if matched:
                key = matched.groups()[0]
                value = matched.groups()[1]
                macros_dict[key] = value
    return macros_dict


def merged_macros(input_macros, default_macros):
    for default_macro in default_macros:
        if default_macro not in input_macros:
            input_macros[default_macro] = default_macros[default_macro]
        # if len(input_macros[default_macro].strip()) == 0 \
        #         and default_macros.get(default_macro) \
        #         and len(default_macros[default_macro]) != 0:
        #     input_macros[default_macro] = default_macros[default_macro]
    return input_macros


def write_macros(macros, filename):
    with open(filename, "w+") as file:
        for key in macros:
            line = "{key}={value}".format(key=key, value=macros[key])
            file.write(line + os.linesep)
