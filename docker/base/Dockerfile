# use the ubuntu base image
FROM ubuntu:16.04

# Acknowledgements to BreakPointSurveyor:
# https://github.com/ding-lab/BreakPointSurveyor/blob/master/docker/Dockerfile

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"

## for apt to be noninteractive
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true


RUN apt-get update && apt-get install -y \
   # Essential
    apt-utils


# Acknowledgements to https://stackoverflow.com/questions/8671308/non-interactive-method-for-dpkg-reconfigure-tzdata:
## preesed tzdata, update package index, upgrade packages and install needed software
RUN echo "tzdata tzdata/Areas select Asia" > /tmp/preseed.txt; \
    echo "tzdata tzdata/Zones/Asia select Chongqing" >> /tmp/preseed.txt; \
    debconf-set-selections /tmp/preseed.txt && \
    rm /etc/timezone && \
    rm /etc/localtime && \
    apt-get update && \
    apt-get install -y tzdata

## cleanup of files from setup
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# install softwares
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    cmake \
    zip \
    unzip \
    curl \
    wget \
    pkg-config \
    vim \
    net-tools \
    iputils-ping \
   # lib
    libbz2-dev \
    liblzma-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
   # Perl related
    cpanminus \
   # R related
    r-base \
   # Python related
    python \
    python-pip \
    python3 \
    python3-pip \
   # Java related
    openjdk-8-jdk \
    openjdk-8-jre \
    && apt-get clean