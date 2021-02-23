#!/usr/bin/env python3
# coding:utf-8

import sys
import json
import os
import shutil
import subprocess
from subprocess import Popen, PIPE

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SOFTWARE_PATH = os.path.join(BASE_DIR, "divis_softwares")

INSTALLED = dict()


def run_shell_cmd(cmdline):
    proc = Popen("bash", stdin=PIPE, stdout=PIPE, stderr=PIPE)
    outs, errs = proc.communicate(cmdline.encode('utf-8'))
    if proc.returncode != 0:
        if outs:
            print(outs.decode('utf-8'))
        if errs:
            print(errs.decode('utf-8'))
        raise Exception("command run error:{}".format(cmdline))
    pass


#  change default software installation path
def change_install_path():
    global SOFTWARE_PATH
    if len(sys.argv) < 2:
        changed = input("DIVIS dependencies will install at {path}, change to (press enter to use default):".format(
            path=SOFTWARE_PATH))
        if len(changed.strip()) > 0:
            if not os.path.exists(changed):
                os.mkdir(changed)
            SOFTWARE_PATH = changed
    else:
        SOFTWARE_PATH = sys.argv[1]
    print("DIVIS dependencies will be installed at {path}".format(path=SOFTWARE_PATH))


#  install base software
def base_software_check():
    print("Check basic software...")
    print("Check python2 ...")
    python2_bin = shutil.which("python2")
    if not python2_bin:
        raise Exception("can't find python2")

    print("Check python3 ...")
    python3_bin = shutil.which("python3")
    if not python3_bin:
        raise Exception("can't find python3")

    _, version = subprocess.getstatusoutput('python3 -V')
    if not float(version.split(" ")[1][:3]) >= 3.5:
        raise Exception("python3 version is less than 3.5")

    print("Check perl ...")
    perl_bin = shutil.which("perl")
    if not perl_bin:
        raise Exception("can't find perl")

    print("Check java ...")
    java_bin = shutil.which("java")
    if not java_bin:
        raise Exception("can't find java")

    print("Check R ...")
    r_bin = shutil.which("R")
    if not r_bin:
        raise Exception("can't find R")

    print("Check basic software ok")


def check_installed():
    global INSTALLED
    skip_file_path = os.path.join(SOFTWARE_PATH, "divis.installed.lock")
    if os.path.exists(skip_file_path):
        with open(skip_file_path, 'r') as skip_file:
            INSTALLED = json.load(skip_file)
    else:
        INSTALLED = {
            "fastp": False,
            "bwa": False,
            "samtools": False,
            "bam_readcount": False,
            "gatk3": False,
            "gatk4": False,
            "picard": False,
            "varscan": False,
            "strelka": False,
            "pindel": False,
            "oncotator": False,
            "gpyflow-cli": False,
        }


def save_installed():
    skip_file_path = os.path.join(SOFTWARE_PATH, "divis.installed.lock")
    with open(skip_file_path, 'w') as skip_file:
        json.dump(INSTALLED, skip_file)


# install pip
def install_requirements():
    print("Install requirements,please wait....")
    install_cmd = '''
pip install -r {base_dir}/divis.requirements.python2.txt --user \
&& pip3 install -r {base_dir}/divis.requirements.python3.txt --user
'''.format(base_dir=BASE_DIR)
    run_shell_cmd(cmdline=install_cmd)
    print("Install requirements finished")


# install bwa
def install_bwa():
    print("Install bwa,please wait....")
    install_cmd = '''
cd {path}
if [ -d "bwa/" ];then
    rm -rf bwa/
fi

git clone https://github.com/lh3/bwa.git \
&& cd bwa \
&& git checkout v0.7.17 \
&& make
'''.format(path=SOFTWARE_PATH)
    run_shell_cmd(cmdline=install_cmd)
    print("Install bwa finished")


# install samtools
def install_samtools():
    print("Install samtools,please wait....")
    install_cmd = '''
cd {path}
if [ -d "samtools-1.8/" ];then
    rm -rf samtools-1.8/
fi

wget https://github.com/samtools/samtools/releases/download/1.8/samtools-1.8.tar.bz2 -O samtools-1.8.tar.bz2 \
&& tar jxvf samtools-1.8.tar.bz2 \
&& cd samtools-1.8 \
&& make
'''.format(path=SOFTWARE_PATH)
    run_shell_cmd(cmdline=install_cmd)
    print("Install samtools finished")


# install bam-readcount
def install_bam_readcount():
    print("Install bam-readcount,please wait....")
    install_cmd = '''
cd {path}
if [ -d "bam-readcount/" ];then
    rm -rf bam-readcount/
fi

git clone https://github.com/genome/bam-readcount.git \
&& cd bam-readcount \
&& git checkout v0.8.0 \
&& mkdir build \
&& cd build \
&& cmake -DCMAKE_INSTALL_PREFIX={path} .. \
&& make
'''.format(path=SOFTWARE_PATH)
    run_shell_cmd(cmdline=install_cmd)
    print("Install bam-readcount finished")


# install fastp
def install_fastp():
    print("Install fastp,please wait....")
    install_cmd = '''
cd {path}
if [ -d "fastp/" ];then
    rm -rf fastp/
fi

git clone https://github.com/OpenGene/fastp.git \
&& cd fastp \
&& git checkout v0.18.0 \
&& make
'''.format(path=SOFTWARE_PATH)
    run_shell_cmd(cmdline=install_cmd)
    print("Install fastp finished")


# install picard
def install_picard():
    print("Install picard,please wait....")
    install_cmd = '''
cd {path}
if [ -d "picard/" ];then
    rm -rf picard/
fi

mkdir picard \
&& cd picard \
&& wget https://github.com/broadinstitute/picard/releases/download/2.18.1/picard.jar -O picard.jar
'''.format(path=SOFTWARE_PATH)
    run_shell_cmd(cmdline=install_cmd)
    print("Install picard finished")


# install gatk3
def install_gatk3():
    print("Install gatk3,please wait....")
    install_cmd = '''
    
cd {path}
if [ -d "gatk3/" ];then
    rm -rf gatk3/
fi

mkdir ./gatk3 \
&& wget "https://software.broadinstitute.org/gatk/download/auth?package=GATK-archive&version=3.7-0-gcfedb67" \
-O GenomeAnalysisTK-3.7.tar.bz2 \
&& tar xf GenomeAnalysisTK-3.7.tar.bz2 -C ./gatk3
'''.format(path=SOFTWARE_PATH)
    run_shell_cmd(cmdline=install_cmd)
    print("Install gatk3 finished")


# install gatk4
def install_gatk4():
    print("Install gatk4,please wait....")
    install_cmd = '''
cd {path}
if [ -d "gatk4/" ];then
    rm -rf gatk4/
fi
wget "https://github.com/broadinstitute/gatk/releases/download/4.0.4.0/gatk-4.0.4.0.zip" -O gatk-4.0.4.0.zip \
&& unzip gatk-4.0.4.0.zip \
&& mv ./gatk-4.0.4.0 gatk4/
'''.format(path=SOFTWARE_PATH)
    run_shell_cmd(cmdline=install_cmd)
    print("Install gatk4 finished")


# install varscan
def install_varscan():
    print("Install varscan,please wait....")
    install_cmd = '''
cd {path}
if [ -d "varscan/" ];then
    rm -rf varscan/
fi

mkdir varscan \
&& wget "https://github.com/dkoboldt/varscan/releases/download/2.4.2/VarScan.v2.4.2.jar" -O VarScan.v2.4.2.jar \
&& mv ./VarScan.v2.4.2.jar varscan/varscan.jar
'''.format(path=SOFTWARE_PATH)
    run_shell_cmd(cmdline=install_cmd)
    print("Install varscan finished")


# install strelka
def install_strelka():
    print("Install strelka,please wait....")
    install_cmd = '''
cd {path}
if [ -d "strelka_workflow-1.0.15/" ];then
    rm -rf strelka_workflow-1.0.15/
fi

wget -c ftp://strelka:%27%27@ftp.illumina.com/v1-branch/v1.0.15/strelka_workflow-1.0.15.tar.gz -O strelka_workflow-1.0.15.tar.gz\
&& tar xvf strelka_workflow-1.0.15.tar.gz \
&& cd strelka_workflow-1.0.15 \
&& ./configure --prefix={path}/strelka\
&& make
'''.format(path=SOFTWARE_PATH)
    run_shell_cmd(cmdline=install_cmd)
    print("Install strelka finished")


# install pindel
def install_pindel():
    print("Install pindel,please wait....")
    install_cmd = '''
cd {path}
if [ -d "htslib/" ];then
    rm -rf htslib/
fi
git clone https://github.com/samtools/htslib.git \
&& cd htslib \
&& git checkout 1.9 \
&& autoheader \
&& autoconf  \
&& ./configure \
&& make \

cd {path}
if [ -d "pindel/" ];then
    rm -rf pindel/
fi

git clone https://github.com/ding-lab/pindel.git \
&& cd pindel \
&& git checkout fba5bbcdc735da6d253b2f0bd5eaff113a4e3a69 \
&& ./INSTALL ../htslib/
'''.format(path=SOFTWARE_PATH)
    run_shell_cmd(cmdline=install_cmd)
    print("Install pindel finished")


# install oncotator
def install_oncotator():
    print("Install oncotator,please wait....")
    install_cmd = '''
cd {path}
if [ -d "oncotator/" ];then
    rm -rf oncotator/
fi

git clone https://github.com/broadinstitute/oncotator.git \
&& cd oncotator \
&& git checkout v1.9.1.0 \
&& python setup.py install --user
'''.format(path=SOFTWARE_PATH)
    run_shell_cmd(cmdline=install_cmd)
    print("Install oncotator finished")


# install gpyflow-cli
def install_gpyflow_cli():
    print("Install GPyFlow-CLI,please wait....")
    install_cmd = '''
    cd {path}
    if [ -d "GPyFlow-CLI/" ];then
        rm -rf GPyFlow-CLI/
    fi

    git clone https://github.com/niu-lab/GPyFlow-CLI.git \
    && cd GPyFlow-CLI \
    && python3 setup.py install --user
    '''.format(path=SOFTWARE_PATH)
    run_shell_cmd(cmdline=install_cmd)
    print("Install GPyFlow-CLI finished")


INSTALL_FUNCS = {
    "fastp": install_fastp,
    "bwa": install_bwa,
    "samtools": install_samtools,
    "bam_readcount": install_bam_readcount,
    "gatk3": install_gatk3,
    "gatk4": install_gatk4,
    "picard": install_picard,
    "varscan": install_varscan,
    "strelka": install_strelka,
    "pindel": install_pindel,
    "oncotator": install_oncotator,
    "gpyflow-cli": install_gpyflow_cli,
}


def install_dependencies():
    # install requirements first
    for dependency in INSTALLED:
        if not INSTALLED[dependency]:
            try:
                INSTALL_FUNCS[dependency]()
            except Exception as e:
                print("install {} failed".format(dependency))
                print(e)
                save_installed()
                exit(1)
            INSTALLED[dependency] = True
            print("install {} success".format(dependency))
            save_installed()
        else:
            print("skip {}".format(dependency))
    print("Install all dependencies success, have a good day. :)")


if __name__ == '__main__':
    base_software_check()
    change_install_path()
    check_installed()
    install_requirements()
    install_dependencies()
