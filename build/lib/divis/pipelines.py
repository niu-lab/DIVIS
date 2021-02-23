import sys
import os
from divis.utils import dir_create
from divis.flows import FLOWS_DICT
from divis.macros import DEFAULT_MACROS_DICT
from divis.macros import read_macros, write_macros
from divis.steps import flow_run
from multiprocessing import Process


def somatic_pipeline(preview, input_macros_file, out_dir):
    # create out directory
    out_dir = os.path.abspath(out_dir)
    dir_create(out_dir)
    total_macros = read_macros(input_macros_file)
    # align
    normal_r1 = total_macros.get("NORMAL_R1")
    if not normal_r1:
        sys.stderr.write("can't find NORMAL_R1" + os.linesep)
        exit(1)
    normal_r2 = total_macros.get("NORMAL_R2")
    if not normal_r2:
        sys.stderr.write("can't find NORMAL_R2" + os.linesep)
        exit(1)

    tumor_r1 = total_macros.get("TUMOR_R1")
    if not tumor_r1:
        sys.stderr.write("can't find TUMOR_R1" + os.linesep)
        exit(1)
    tumor_r2 = total_macros.get("TUMOR_R2")
    if not tumor_r2:
        sys.stderr.write("can't find TUMOR_R2" + os.linesep)
        exit(1)

    sample_name = total_macros.get("SAMPLE_NAME")
    if not sample_name:
        sys.stderr.write("can't find SAMPLE_NAME" + os.linesep)
        exit(1)

    platform = total_macros.get("PLATFORM")
    if not platform:
        sys.stderr.write("can't find PLATFORM" + os.linesep)
        exit(1)

    normal_rg = '\'@RG\\tID:{sample_name}_N\\tSM:{sample_name}_N\\tLB:{sample_name}_N\\tPL:{platform}\''.format(
        sample_name=sample_name,
        platform=platform)

    tumor_rg = '\'@RG\\tID:{sample_name}_T\\tSM:{sample_name}_T\\tLB:{sample_name}_T\\tPL:{platform}\''.format(
        sample_name=sample_name,
        platform=platform)

    align_macros = read_macros(DEFAULT_MACROS_DICT.get("align"))
    for align_macro in align_macros:
        if align_macro in total_macros:
            align_macros[align_macro] = total_macros[align_macro]

    # normal align macro
    align_macros["R1"] = normal_r1
    align_macros["R2"] = normal_r2
    align_macros["RG"] = normal_rg
    align_macros["SAMPLE_NAME"] = "{}_normal".format(sample_name)
    normal_macros_file = os.path.join(out_dir, "normal.align.macros")
    write_macros(align_macros, normal_macros_file)
    # tumor align macros
    align_macros["R1"] = tumor_r1
    align_macros["R2"] = tumor_r2
    align_macros["RG"] = tumor_rg
    align_macros["SAMPLE_NAME"] = "{}_tumor".format(sample_name)
    tumor_macros_file = os.path.join(out_dir, "tumor.align.macros")
    write_macros(align_macros, tumor_macros_file)

    # normal align
    normal_align_dir = os.path.join(out_dir, "normal_align")
    print("------ normal align ------")
    normal_align_thread = Process(target=flow_run,
                                  args=(preview,
                                        FLOWS_DICT.get("align"),
                                        normal_macros_file,
                                        normal_align_dir))
    normal_align_thread.start()

    # tumor align
    tumor_align_dir = os.path.join(out_dir, "tumor_align")
    print("------ tumor align ------")
    tumor_align_thread = Process(target=flow_run,
                                 args=(preview,
                                       FLOWS_DICT.get("align"),
                                       tumor_macros_file,
                                       tumor_align_dir))
    tumor_align_thread.start()

    normal_align_thread.join()
    tumor_align_thread.join()

    # VSP variants calling
    # varscan somatic
    # print("------ varscan somatic ------")
    # varscan_somatic_macros = read_macros(DEFAULT_MACROS_DICT.get("varscan_somatic"))
    # for macro in varscan_somatic_macros:
    #     if macro in total_macros:
    #         varscan_somatic_macros[macro] = total_macros[macro]
    #
    # varscan_somatic_macros["NORMAL_BAM"] = os.path.join(normal_align_dir, "{}_normal.bam".format(sample_name))
    # varscan_somatic_macros["TUMOR_BAM"] = os.path.join(tumor_align_dir, "{}_tumor.bam".format(sample_name))
    # varscan_somatic_macros_file = os.path.join(out_dir, "varscan_somatic.macros")
    # write_macros(varscan_somatic_macros, varscan_somatic_macros_file)
    # varscan_somatic_dir = os.path.join(out_dir, "varscan_somatic")
    # varscan_thread = Process(target=flow_run, args=(preview, FLOWS_DICT.get("varscan_somatic"),
    #                                                 varscan_somatic_macros_file,
    #                                                 varscan_somatic_dir))
    # varscan_thread.start()
    #
    # # strelka somatic
    # print("------ strelka somatic ------")
    # strelka_somatic_macros = read_macros(DEFAULT_MACROS_DICT.get("strelka_somatic"))
    # for macro in strelka_somatic_macros:
    #     if macro in total_macros:
    #         strelka_somatic_macros[macro] = total_macros[macro]
    #
    # strelka_somatic_macros["NORMAL_BAM"] = os.path.join(normal_align_dir, "{}_normal.bam".format(sample_name))
    # strelka_somatic_macros["TUMOR_BAM"] = os.path.join(tumor_align_dir, "{}_tumor.bam".format(sample_name))
    # strelka_somatic_macros_file = os.path.join(out_dir, "strelka_somatic.macros")
    # write_macros(strelka_somatic_macros, strelka_somatic_macros_file)
    # strelka_somatic_dir = os.path.join(out_dir, "strelka_somatic")
    # strelka_thread = Process(target=flow_run, args=(preview, FLOWS_DICT.get("strelka_somatic"),
    #                                                 strelka_somatic_macros_file,
    #                                                 strelka_somatic_dir))
    # strelka_thread.start()
    #
    # # pindel somatic
    # print("------ pindel somatic ------")
    # pindel_somatic_macros = read_macros(DEFAULT_MACROS_DICT.get("pindel_somatic"))
    # for macro in pindel_somatic_macros:
    #     if macro in total_macros:
    #         pindel_somatic_macros[macro] = total_macros[macro]
    #
    # pindel_somatic_macros["NORMAL_BAM"] = os.path.join(normal_align_dir, "{}_normal.bam".format(sample_name))
    # pindel_somatic_macros["TUMOR_BAM"] = os.path.join(tumor_align_dir, "{}_tumor.bam".format(sample_name))
    # pindel_somatic_macros_file = os.path.join(out_dir, "pindel_somatic.macros")
    # write_macros(pindel_somatic_macros, pindel_somatic_macros_file)
    # pindel_somatic_dir = os.path.join(out_dir, "pindel_somatic")
    # pindel_thread = Process(target=flow_run, args=(preview,
    #                                                FLOWS_DICT.get("pindel_somatic"),
    #                                                pindel_somatic_macros_file,
    #                                                pindel_somatic_dir))
    # pindel_thread.start()
    #
    # varscan_thread.join()
    # strelka_thread.join()
    # pindel_thread.join()
    #
    # # annotation
    # print("------ oncotator annotation ------")
    # oncotator_macros = read_macros(DEFAULT_MACROS_DICT.get("oncotator"))
    # for macro in oncotator_macros:
    #     if macro in total_macros:
    #         oncotator_macros[macro] = total_macros[macro]
    #
    # vcfs = "{varscan_dir}/{sample_name}.indel.vcf " \
    #        "{varscan_dir}/{sample_name}.snp.vcf " \
    #        "{strelka_dir}/strelk_out/results/passed.somatic.indels.vcf " \
    #        "{strelka_dir}/strelk_out/results/passed.somatic.snvs.vcf " \
    #        "{pindel_dir}/{sample_name}.somatic.delete.vcf " \
    #        "{pindel_dir}/{sample_name}.somatic.insert.vcf ".format(varscan_dir=varscan_somatic_dir,
    #                                                                strelka_dir=strelka_somatic_dir,
    #                                                                pindel_dir=pindel_somatic_dir,
    #                                                                sample_name=sample_name)
    # oncotator_macros["VCFS"] = vcfs
    # oncotator_macros["NORMAL_BARCODE"] = "{}_normal".format(sample_name)
    # oncotator_macros["TUMOR_BARCODE"] = "{}_tumor".format(sample_name)
    # oncotator_macros_file = os.path.join(out_dir, "oncotator.macros")
    # write_macros(oncotator_macros, oncotator_macros_file)
    # oncotator_dir = os.path.join(out_dir, "oncotator")
    # oncotator_thread = Process(target=flow_run, args=(preview, FLOWS_DICT.get("oncotator"),
    #                                                   oncotator_macros_file,
    #                                                   oncotator_dir))
    # oncotator_thread.start()
    # oncotator_thread.join()
    pass


def gatk4_haplotypecaller_germline_pipeline(preview, in_macro_file, out_dir):
    # create out directory
    out_dir = os.path.abspath(out_dir)
    dir_create(out_dir)
    total_macros = read_macros(in_macro_file)

    # quality control
    qc_macros = read_macros(DEFAULT_MACROS_DICT.get("qc"))

    for qc_macro in qc_macros:
        if qc_macro in total_macros:
            qc_macros[qc_macro] = total_macros[qc_macro]

    qc_macros_file = os.path.join(out_dir, "qc.macros")
    write_macros(qc_macros, qc_macros_file)
    qc_dir = os.path.join(out_dir, "qc")
    print("------ quality control ------")
    flow_run(preview, FLOWS_DICT.get("qc"), qc_macros_file, qc_dir)

    # alignment
    align_macros = read_macros(DEFAULT_MACROS_DICT.get("align"))
    for align_macro in align_macros:
        if align_macro in total_macros:
            align_macros[align_macro] = total_macros[align_macro]

    sample_name = total_macros.get("SAMPLE_NAME")
    platform = total_macros.get("PLATFORM")
    rg = '\'@RG\\tID:{sample_name}\\tSM:{sample_name}\\tLB:{sample_name}\\tPL:{platform}\''.format(
        sample_name=sample_name,
        platform=platform)
    align_macros["RG"] = rg

    align_macros_file = os.path.join(out_dir, "align.macros")
    write_macros(align_macros, align_macros_file)
    align_dir = os.path.join(out_dir, "align")
    print("------ align ------")
    flow_run(preview, FLOWS_DICT.get("align"), align_macros_file, align_dir)

    # variants calling

    bam_file = os.path.join(align_dir, "{}.bam".format(sample_name))

    gatk4_haplotypecaller_macros = read_macros(DEFAULT_MACROS_DICT.get("gatk4_haplotypecaller_germline"))

    for gatk4_haplotypecaller_macro in gatk4_haplotypecaller_macros:
        if gatk4_haplotypecaller_macro in total_macros:
            gatk4_haplotypecaller_macros[gatk4_haplotypecaller_macro] = total_macros[gatk4_haplotypecaller_macro]

    gatk4_haplotypecaller_macros["BAM_FILE"] = bam_file

    gatk4_haplotypecaller_macros_file = os.path.join(out_dir, "gatk4_haplotypecaller_germline.macros")
    write_macros(gatk4_haplotypecaller_macros, gatk4_haplotypecaller_macros_file)
    gatk4_haplotypecaller_dir = os.path.join(out_dir, "gatk4_haplotypecaller")
    print("------ variants calling ------")
    flow_run(preview, FLOWS_DICT.get("gatk4_haplotypecaller_germline"), gatk4_haplotypecaller_macros_file,
             gatk4_haplotypecaller_dir)

    pass


PIPELINE_FUNCS = {
    "wes_somatic": somatic_pipeline,
    "wgs_somatic": somatic_pipeline,
    "panel_germline": gatk4_haplotypecaller_germline_pipeline,
}


def pipeline_run(pipeline_name, preview, input_macros_file, out_dir):
    func = PIPELINE_FUNCS.get(pipeline_name)
    if not func:
        sys.stderr.write("can't find {} pipeline".format(pipeline_name) + os.linesep)
    func(preview, input_macros_file, out_dir)
