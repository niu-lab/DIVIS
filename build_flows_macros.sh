#!/usr/bin/env bash

set -e

CURDIR=`pwd`

# install GPyFlow
echo "--- install GPyFLow-CLI ---"
if [ -d "vendor/GPyFlow-CLI" ]
then
    cd vendor/GPyFlow-CLI 
    #git pull > /dev/null 2>&1 
    python3 setup.py install > /dev/null 2>&1
else
    #git clone https://github.com/niu-lab/GPyFlow-CLI.git vendor/GPyFlow-CLI > /dev/null 2>&1
    cd vendor/GPyFlow-CLI && python3 setup.py install > /dev/null 2>&1
fi

cd ${CURDIR}

RUN_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
SUBSTEPS_FLOW_DIR=${RUN_DIR}/divis/flows/substeps
PIPELINES_FLOWS_DIR=${RUN_DIR}/divis/flows/pipelines
SUBSTEPS_MACROS_DIR=${RUN_DIR}/divis/macros/tpl/substeps
PIPELINES_MACROS_DIR=${RUN_DIR}/divis/macros/tpl/pipelines

echo "--- clean all build file ---"
echo "rm -rf ${SUBSTEPS_FLOW_DIR}/*.zip"
rm -rf ${SUBSTEPS_FLOW_DIR}/*.zip
echo "rm -rf ${PIPELINES_FLOWS_DIR}/*.zip"
rm -rf ${PIPELINES_FLOWS_DIR}/*.zip
echo "rm -rf ${SUBSTEPS_MACROS_DIR}/*.macros"
rm -rf ${SUBSTEPS_MACROS_DIR}/*.macros
echo "rm -rf ${PIPELINES_MACROS_DIR}/*.macros"
rm -rf ${PIPELINES_MACROS_DIR}/*.macros


echo "--- build substeps zip file ---"
echo "cd ${SUBSTEPS_FLOW_DIR}"
cd ${SUBSTEPS_FLOW_DIR}
for name in `ls .`
do
    if test -d ${name}
    then
        echo "pyflow tar ${name}"
        pyflow tar ${name}
    fi
done

echo "--- extract substep macros ---"
echo "cd ${SUBSTEPS_FLOW_DIR}"
cd ${SUBSTEPS_FLOW_DIR}
for name in `ls .`
do
    if test -d ${name}
    then
        echo "pyflow extract -f ${name}/flow.json ${SUBSTEPS_MACROS_DIR}/${name}.macros"
        pyflow extract -f ${name}/flow.json ${SUBSTEPS_MACROS_DIR}/${name}.macros
    fi
done


echo "--- merge substeps to pipeline ---"
wes_somatic_need_macros=("align" "varscan_somatic" "strelka_somatic" "pindel_somatic" "vardict_somatic")
for macro in ${wes_somatic_need_macros[*]}
do
    echo "cp ${SUBSTEPS_MACROS_DIR}/${macro}.macros ${PIPELINES_FLOWS_DIR}/wes_somatic/tpl"
    cp ${SUBSTEPS_MACROS_DIR}/${macro}.macros ${PIPELINES_FLOWS_DIR}/wes_somatic/tpl
done



echo "--- build pipeline zip file ---"
echo "cd ${PIPELINES_FLOWS_DIR}"
cd ${PIPELINES_FLOWS_DIR}
for name in `ls .`
do
    if test -d ${name}
    then
        echo "pyflow tar ${name}"
        pyflow tar ${name}
    fi
done

echo "--- extract pipeline macros ---"
echo "cd ${PIPELINES_FLOWS_DIR}"
cd ${PIPELINES_FLOWS_DIR}
for name in `ls .`
do
    if test -d ${name}
    then
        echo "pyflow extract -f ${name}/flow.json ${PIPELINES_MACROS_DIR}/${name}.macros"
        pyflow extract -f ${name}/flow.json ${PIPELINES_MACROS_DIR}/${name}.macros
    fi
done
