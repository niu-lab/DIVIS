#!/usr/bin/env python3

import click

tpl = '''[manual_annotations]
override:Center={center},tumor_barcode={tumor_barcode},normal_barcode={normal_barcode},Strand=+,NCBI_Build={ncbi_build},source={source},phase=annotation,sequencer={sequencer},Mutation_Status={mutattion_status}'''


@click.command()
@click.option('--sample_name', required=True, help="Sample Name", type=str)
@click.option('--normal_barcode', required=True, help="Normal Barcode", type=str)
@click.option('--tumor_barcode', required=True, help="Tumor Barcode", type=str)
@click.option('--center', required=True, help="Center", type=str)
@click.option('--ncbi_build', required=True, help="NCBI Build,eg:hg19", type=str)
@click.option('--source', required=True, help="Source Type,eg: WES/WGS", type=str)
@click.option('--sequencer', required=True, help="Sequencer,eg:Illumina", type=str)
@click.option('--mutattion_status', required=True, help="Mutation Status,eg:Somatic/Germline", type=str)
def gen_config(sample_name, normal_barcode, tumor_barcode, center, ncbi_build, source, sequencer, mutattion_status):
    config = tpl.format(sample_name=sample_name,
                        normal_barcode=normal_barcode,
                        tumor_barcode=tumor_barcode,
                        center=center,
                        ncbi_build=ncbi_build,
                        source=source,
                        sequencer=sequencer,
                        mutattion_status=mutattion_status)
    file_name = "{}.overrides.config".format(sample_name)
    print(file_name)

    with open(file_name, 'w+') as file:
        file.write(config)


if __name__ == "__main__":
    gen_config()
