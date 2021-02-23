#!/usr/bin/env bash
set -e

# kill runing container
running_container=`docker ps | grep 'divis_web' | awk '{print $1}'`
if [[ ${running_container} != "" ]]
then
    echo "docker kill ${running_container}"
    docker kill ${running_container}
fi


# remove container
running_container=`docker ps -a | grep 'divis_web' | awk '{print $1}'`
if [[ ${running_container} != "" ]]
then
    echo "docker rm ${running_container}"
    docker rm ${running_container}
fi


# build images
divis_image=`docker images | grep -E 'divis\s+0.1' | awk '{print $3}'`
if [[ ${divis_image} != "" ]]
then
    echo "docker rmi ${divis_image}"
    docker rmi ${divis_image}
fi

docker build -t "divis:0.1" .

