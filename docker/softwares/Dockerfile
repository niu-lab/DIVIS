# use the ubuntu base image
FROM divis:base

# fastp
RUN cd /usr/local \
&& git clone https://github.com/OpenGene/fastp.git \
&& cd fastp \
&& git checkout v0.18.0 \
&& make

# bwa
RUN cd /usr/local \
&& git clone https://github.com/lh3/bwa.git \
&& cd bwa \
&& git checkout v0.7.17 \
&& make

# samtools
RUN cd /usr/local \
&& wget https://github.com/samtools/samtools/releases/download/1.8/samtools-1.8.tar.bz2 -O samtools-1.8.tar.bz2 \
&& tar jxvf samtools-1.8.tar.bz2 \
&& cd samtools-1.8 \
&& make

# bam-readcount
RUN cd /usr/local \
&& git clone https://github.com/genome/bam-readcount.git \
&& cd bam-readcount \
&& git checkout v0.8.0 \
&& mkdir build \
&& cd build \
&& cmake -DCMAKE_INSTALL_PREFIX=/usr/local .. \
&& make \
&& make install

# gatk3
RUN cd /usr/local \
&& mkdir ./gatk3 \
&& wget "https://software.broadinstitute.org/gatk/download/auth?package=GATK-archive&version=3.7-0-gcfedb67" \
-O GenomeAnalysisTK-3.7.tar.bz2 \
&& tar xf GenomeAnalysisTK-3.7.tar.bz2 -C ./gatk3

# gatk4
RUN cd /usr/local \
&& wget "https://github.com/broadinstitute/gatk/releases/download/4.0.4.0/gatk-4.0.4.0.zip" -O gatk-4.0.4.0.zip \
&& unzip gatk-4.0.4.0.zip \
&& mv ./gatk-4.0.4.0 gatk4/

# picard
RUN cd /usr/local \
&& mkdir picard \
&& cd picard \
&& wget https://github.com/broadinstitute/picard/releases/download/2.18.1/picard.jar -O picard.jar

# varscan
RUN cd /usr/local \
&& mkdir varscan \
&& wget "https://github.com/dkoboldt/varscan/releases/download/2.4.2/VarScan.v2.4.2.jar" -O VarScan.v2.4.2.jar \
&& mv ./VarScan.v2.4.2.jar varscan/varscan.jar

# strelka
RUN cd /usr/local \
&& wget -c ftp://strelka:%27%27@ftp.illumina.com/v1-branch/v1.0.15/strelka_workflow-1.0.15.tar.gz -O strelka_workflow-1.0.15.tar.gz\
&& tar xvf strelka_workflow-1.0.15.tar.gz \
&& cd strelka_workflow-1.0.15 \
&& ./configure --prefix=/usr/local \
&& make \
&& make install

# pindel
RUN cd /usr/local \
&& git clone https://github.com/samtools/htslib.git \
&& cd htslib \
&& git checkout 1.9 \
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
&& pip install ngslib==1.1.18 \
&& pip install numpy==1.11.0 \
&& pip install pyvcf==0.6.8 \
&& pip install pandas==0.18.0 \
&& pip install biopython==1.66 \
&& cd /usr/local/ \
&& git clone https://github.com/broadinstitute/oncotator.git \
&& cd oncotator \
&& git checkout v1.9.1.0 \
&& python setup.py install

# snp
RUN cd /usr/local \
&& wget https://sourceforge.net/projects/snpeff/files/snpEff_v4_3t_core.zip -O snpEff.zip \
&& unzip snpEff.zip -d snpEff

# vep
RUN apt install -y cpanminus libmysqlclient-dev

RUN cpanm Archive::Zip DBD::mysql DBI

RUN cd /usr/local \
&& curl -L -O https://github.com/Ensembl/ensembl-vep/archive/release/95.zip \
&& unzip 95.zip \
&& cd ensembl-vep-release-95/ \
&& perl ./INSTALL.pl -a a -l

# joinx
COPY ./joinx /usr/local/bin