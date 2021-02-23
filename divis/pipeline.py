import os
from divis.flows import PIPELINE_FLOWS_DICT
from divis.substep import flow_run


def pipeline_run(pipeline_name, preview, input_macros_file, out_dir):
    if pipeline_name not in PIPELINE_FLOWS_DICT.keys():
        print("can't find pipeline: {}".format(pipeline_name))
        exit(1)
    input_macros_file = os.path.abspath(input_macros_file)
    out_dir = os.path.abspath(out_dir)
    pipeline_flow = PIPELINE_FLOWS_DICT.get(pipeline_name)
    flow_run(preview, pipeline_flow, input_macros_file, out_dir)
