import os
from divis.flows import SUBSTEPS_FLOWS_DICT
from divis.macros import DEFAULT_SUBSTEP_MACROS_DICT
from divis.macros import read_macros, merged_macros, write_macros
from GPyFlow.workflow import run_target
from divis.utils import dir_create


def flow_run(preview, flow, inputs_file, out_dir):
    run_target(preview, flow, inputs_file, out_dir)


def sub_step_run(step_name, preview, input_macros_file, out_dir):
    if step_name not in SUBSTEPS_FLOWS_DICT.keys():
        print("can't find sub step: {}".format(step_name))
        exit(1)
    default_macros_file = DEFAULT_SUBSTEP_MACROS_DICT[step_name]
    # read macros
    input_macros = read_macros(input_macros_file)
    default_macros = read_macros(default_macros_file)
    # merge macros
    merged = merged_macros(input_macros, default_macros)
    # create dir
    dir_create(out_dir)
    # write macros file
    inputs_file = os.path.join(out_dir, "{step_name}.macros".format(step_name=step_name))
    write_macros(merged, inputs_file)
    # run flow
    step_flow = SUBSTEPS_FLOWS_DICT[step_name]
    step_dir = os.path.join(out_dir, step_name)
    flow_run(preview, step_flow, inputs_file, step_dir)
