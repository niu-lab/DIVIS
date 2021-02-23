import os
from divis.config import BASE_DIR

FLOWS_ROOT = os.path.join(BASE_DIR, "flows")

SUBSTEPS_FLOWS_ROOT = os.path.join(FLOWS_ROOT, "substeps")

PIPELINE_FLOWS_ROOT = os.path.join(FLOWS_ROOT, "pipelines")

SUBSTEPS_FLOWS_DICT = {
    "qc": os.path.join(SUBSTEPS_FLOWS_ROOT, "qc.zip"),
    "qc_to_align": os.path.join(SUBSTEPS_FLOWS_ROOT, "qc_to_align.zip"),
    "align": os.path.join(SUBSTEPS_FLOWS_ROOT, "align.zip"),
    "varscan_somatic": os.path.join(SUBSTEPS_FLOWS_ROOT, "varscan_somatic.zip"),
    "strelka_somatic": os.path.join(SUBSTEPS_FLOWS_ROOT, "strelka_somatic.zip"),
    "pindel_somatic": os.path.join(SUBSTEPS_FLOWS_ROOT, "pindel_somatic.zip"),
    "vardict_somatic": os.path.join(SUBSTEPS_FLOWS_ROOT, "vardict_somatic.zip"),
    "gatk4_haplotypecaller_germline": os.path.join(SUBSTEPS_FLOWS_ROOT, "gatk4_haplotypecaller_germline.zip"),
    "oncotator": os.path.join(SUBSTEPS_FLOWS_ROOT, "oncotator.zip"),
    "mutect1_somatic":os.path.join(SUBSTEPS_FLOWS_ROOT, "mutect1_somatic.zip"),
    "vep":os.path.join(SUBSTEPS_FLOWS_ROOT, "vep.zip"),
    "divis_report":os.path.join(SUBSTEPS_FLOWS_ROOT, "divis_report.zip")
}

PIPELINE_FLOWS_DICT = {
    "wes_somatic": os.path.join(PIPELINE_FLOWS_ROOT, "wes_somatic.zip")
}
