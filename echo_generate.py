#!/usr/bin/env python3
import os
from divis.flows import PIPELINE_FLOWS_ROOT
from divis.macros import read_macros

skips = ["R1", "R2", "TUMOR_BAM", "NORMAL_BAM", "RG"]
adds = ["NORMAL_R1", "NORMAL_R2", "TUMOR_R1", "TUMOR_R2", "PLATFORM"]


def echo():
    tpl_dir = os.path.join(PIPELINE_FLOWS_ROOT, 'wes_somatic/tpl')
    macros = dict()
    for item in os.listdir(tpl_dir):
        macro_file = os.path.join(tpl_dir, item)
        tmp = read_macros(macro_file)
        macros = dict(macros, **tmp)

    macros_names = adds + list(macros.keys())
    for macro in sorted(macros_names):
        if macro in skips:
            continue
        print("echo \"{macro}=#{macro}#\" >> required.macros".format(macro=macro))


def main():
    echo()


if __name__ == "__main__":
    main()
