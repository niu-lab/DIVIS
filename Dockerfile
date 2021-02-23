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
    autoconf \
    automake \
   # lib
    libbz2-dev \
    liblzma-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libcurl4-gnutls-dev \
    libssl-dev \
    libopenblas-base \
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

# fastqc
RUN cd /usr/local/ \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/fastqc_v0.11.9.zip -O fastqc_v0.11.9.zip \
&& unzip fastqc_v0.11.9.zip \
&& chmod a+x /usr/local/FastQC/fastqc

# fastp
RUN cd /usr/local \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/fastp-0.20.0.tar.gz -O fastp-0.20.0.tar.gz \
&& tar xvf fastp-0.20.0.tar.gz \
&& cd fastp-0.20.0 \
&& make

# bwa
RUN cd /usr/local \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/bwa-0.7.17.tar.bz2 -O bwa-0.7.17.tar.bz2 \
&& tar jxvf bwa-0.7.17.tar.bz2 \
&& cd bwa-0.7.17 \
&& make

# samtools
RUN cd /usr/local \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/samtools-1.11.tar.bz2 -O samtools-1.11.tar.bz2 \
&& tar jxvf samtools-1.11.tar.bz2 \
&& cd samtools-1.11 \
&& make

# bam-readcount
RUN cd /usr/local \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/bam-readcount-0.8.0.tar.gz -O bam-readcount-0.8.0.tar.gz \
&& tar xvf bam-readcount-0.8.0.tar.gz \
&& cd bam-readcount-0.8.0 \
&& mkdir build \
&& cd build \
&& cmake -DCMAKE_INSTALL_PREFIX=/usr/local .. \
&& make \
&& make install

# gatk3
RUN cd /usr/local \
&& mkdir ./gatk3 \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/GenomeAnalysisTK-3.7.tar.bz2 -O GenomeAnalysisTK-3.7.tar.bz2 \
&& tar xf GenomeAnalysisTK-3.7.tar.bz2 -C ./gatk3

# gatk4
RUN cd /usr/local \
&& mkdir ./gatk4 \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/gatk-4.1.9.0.zip -O gatk-4.1.9.0.zip \
&& unzip gatk-4.1.9.0.zip \
&& mv ./gatk-4.1.9.0.zip gatk4/

# picard
RUN cd /usr/local \
&& mkdir picard \
&& cd picard \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/picard.2.25.0.jar -O picard.jar

# varscan
RUN cd /usr/local \
&& mkdir varscan \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/VarScan.v2.4.2.jar -O VarScan.v2.4.2.jar \
&& mv ./VarScan.v2.4.2.jar varscan/varscan.jar

# strelka
RUN cd /usr/local \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/strelka_workflow-2.9.10.tar.gz -O strelka_workflow-2.9.10.tar.gz\
&& tar xvf strelka_workflow-2.9.10.tar.gz \
&& cd strelka-2.9.10 \
&& mkdir build \
&& cd build \
&& ../configure --prefix=/usr/local \
&& make \
&& make install

# pindel
RUN cd /usr/local \
&& git clone https://github.com/samtools/htslib.git \
&& cd htslib \
&& git checkout 1.11 \
&& autoheader \
&& autoconf  \
&& ./configure \
&& make \
&& cd /usr/local \
&& git clone https://github.com/ding-lab/pindel.git \
&& cd pindel \
&& git checkout fba5bbcdc735da6d253b2f0bd5eaff113a4e3a69 \
&& ./INSTALL ../htslib/

# oncototor
RUN pip install bcbio-gff==0.6.2 \
&& pip install pysam==0.9.0 \
&& pip install cython==0.24 \
&& pip install shove==0.6.6 \
&& pip install sqlalchemy==1.0.12 \
&& pip install nose==1.3.7 \
&& pip install python-memcached==1.57 \
&& pip install natsort==4.0.4 \
&& pip install more-itertools==2.2 \
&& pip install enum34==1.1.2 \
&& pip install numpy==1.11.0 \
&& pip install ngslib==1.1.18 \
&& pip install pyvcf==0.6.8 \
&& pip install pandas==0.18.0 \
&& pip install biopython==1.66 \
&& cd /usr/local/ \
&& git clone https://github.com/broadinstitute/oncotator.git \
&& cd oncotator \
&& git checkout v1.9.1.0 \
&& python setup.py install

# SnpSift.jar
RUN cd /usr/local \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/snpEff.v4.3.zip -O snpEff.zip \
&& unzip snpEff.zip -d snpEff

# VarDictJava
RUN cd /usr/local/ \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/VarDict-1.8.2.tar -O VarDict-1.8.2.tar \
&& tar xvf VarDict-1.8.2.tar

# vep
RUN apt install -y cpanminus libmysqlclient-dev

RUN cpanm Archive::Zip DBD::mysql DBI

RUN cd /usr/local \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/vep.95.zip -O  vep.95.zip \
&& unzip vep.95.zip \
&& cd ensembl-vep-release-95/ \
&& perl ./INSTALL.pl -a a -l -n

# annovar
RUN cd /usr/local/ \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/annovar.latest.tar.gz \
&& tar xvf annovar.latest.tar.gz

# joinx
RUN cd /usr/local/bin \
&& wget http://niulab.scgrid.cn/dataserver/data/softwares/joinx

#DIVIS 
RUN mkdir /opt/DIVISPipeline
COPY . /opt/DIVISPipeline/

RUN cd /usr/local \
&& git clone https://github.com/niu-lab/GPyFlow-CLI.git \
&& cd GPyFlow-CLI \
&& python3 setup.py install

RUN cd /opt/DIVISPipeline/ \
&& pip3 install click==5.1 \
&& python3 setup.py install

ENV FLASK_CONFIG="production"
