#!/usr/bin/env python3

import click
from divis.flows import SUBSTEPS_FLOWS_DICT, PIPELINE_FLOWS_DICT
from divis.substep import sub_step_run
from divis.pipeline import pipeline_run


@click.group()
def cli():
    pass


@click.command()
@click.option('--step', '-s', required=True,
              help="Run sub step:[{}]".format(",".join(list(SUBSTEPS_FLOWS_DICT.keys()))))
@click.option('--preview', '-p', is_flag=True, help="Preview commands")
@click.option('--config_file', '-c', required=True, help="Input config file")
@click.option('--out_dir', '-o', required=True, help="Output directory")
def substep(step, preview, config_file, out_dir):
    """do sub step."""
    sub_step_run(step, preview, config_file, out_dir)


@click.command()
@click.option('--worklflow', '-f', required=True,
              help="Run workflow:[{}]".format(",".join(list(PIPELINE_FLOWS_DICT.keys()))))
@click.option('--preview', '-p', is_flag=True, help="Preview commands")
@click.option('--config_file', '-c', required=True, help="Input config file")
@click.option('--out_dir', '-o', required=True, help="Output directory")
def pipeline(worklflow, preview, config_file, out_dir):
    """do auto workflow."""
    pipeline_run(worklflow, preview, config_file, out_dir)


cli.add_command(substep)
cli.add_command(pipeline)


def main():
    cli()


if __name__ == '__main__':
    main()
