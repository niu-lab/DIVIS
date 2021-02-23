# Introduction

***DIVIS***，an easy-to-use, extensible, and customisable cancer genome sequencing analysis platform which including the functions of variant Detection, Interpretation, Visualisation, and one can use DIVIS as an infrastructure of genome analysis. 



DIVIS can run in single sample (see Single sample mode section) and paired sample (see Paired variant calling section). As input, DIVIS takes a config files which contains reference genomes in FASTA format, sequencing reads in FASTQ format or aligned reads in BAM format, and target regions in BED format, *ect.*



# Get DIVIS

## 1. Local Installation

### Prerequisites

- [GPyFlow](http://niulab.scgrid.cn/GPyFlow/)
- Java 1.8
- Python 2.7+
- Python 3.5+
- R 3.2+
- Perl 5.22+

### Software Dependencies

DIVIS currently covers software of all stages of cancer genome sequencing, Users need to preinstall these software: 

***Required***: 

1. [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/),  
2. [Fastp](https://github.com/OpenGene/fastp), 
3. [bwa](https://github.com/lh3/bwa),
4. [samtools](http://www.htslib.org/), 
5. [GATK](https://gatk.broadinstitute.org/hc/en-us), 
6. [VarDict](https://github.com/AstraZeneca-NGS/VarDict), 
7. [Strelka](https://github.com/Illumina/strelka), 
8. [VarScan2](http://varscan.sourceforge.net/), 

***Optinal:***  

1. [Annovar](https://annovar.openbioinformatics.org/en/latest/), 
2. [Ensembl Variant Effect Predictor (VEP)](https://www.ensembl.org/vep)

or run the following command  directly:

```
git clone https://github.com/niu-lab/DIVIS.git
cd DIVIS
python3 install.py [divis-dependent-softwares-install-path]
python3 setup.py install
```

## 2. Docker 

***Note*** Due to the difficulty (i.e. no root access to install required libraries or incompatible libraries) in running DIVIS, we have made a docker image available at [Docker Hub](https://hub.docker.com/), which contains the **latest development version** of DIVIS and all dependent libraries. 

# Run DIVIS

DIVIS includes two functional modules: 'pipeline' and 'substep' :

```
Usage: divis [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  pipeline  do auto workflow.
  substep   do sub step.

```

## pipeline: 

```
Usage: divis pipeline [OPTIONS]

  do auto workflow.

Options:
  -f, --worklflow TEXT    Run workflow:[wes_somatic,wes_germline,wgs_somatic,wgs_germline]  [required]
  -p, --preview           Preview commands
  -c, --config_file TEXT  Input config file  [required]
  -o, --out_dir TEXT      Output directory  [required]
  --help                  Show this message and exit.

```

## substep:

```
Usage: divis substep [OPTIONS]

  do sub step.

Options:
  -s, --step TEXT         Run sub step:[qc,qc_to_align,align,varscan_somatic,s
                          trelka_somatic,pindel_somatic,vardict_somatic,gatk4_
                          haplotypecaller_germline,oncotator,mutect1_somatic,v
                          ep,divis_report]  [required]
  -p, --preview           Preview commands
  -c, --config_file TEXT  Input config file  [required]
  -o, --out_dir TEXT      Output directory  [required]
  --help                  Show this message and exit.
```

## Input

Both '**pipeline**' and '**substep**' commands require a **project-specific configuration file**, which consists of key value pairs with ***"key = value"***.  Configuration templates and default settings are stored in [./divis/macros](https://github.com/niu-lab/DIVISPipelineSRC/divis/macros) .You should edit the configuration file with software path, software parameters, input FASTQ/BAM/VCF/MAF files, reference genome and settings of output.  For example (TEST.align.config):

```
BWA=/bin/bwa
SAMTOOLS=bin/samtools
PICARD=/bin/picard.jar
GATK3=/bin/gatk3/GenomeAnalysisTK.jar
GATK4=/bin/gatk4/gatk
THREAD=8
RG="@RG\tID:TEST\tLB:TEST\tSM:TEST\tPL:Illumina"
GATK3_REALIGN_PARAS=-known 1000G_phase1.indels.hg19.sites.vcf -known Mills_and_1000G_gold_standard.indels.hg19.sites.vcf --intervals S07604514_Padded.bed
GATK4_BASERECALIBRATE_PARAMS=--known-sites 1000G_phase1.indels.hg19.sites.vcf --known-sites Mills_and_1000G_gold_standard.indels.hg19.sites.vcf --intervals S07604514_Padded.bed
REF=ucsc.hg19.fasta
SAMPLE_NAME=TEST
TMP=./TEST
R1=TEST.1.fastq.gz
R2=TEST.2.fastq.gz
```

An example of DIVIS subtep "align": 

```
divis substep -s align -c ./TEST.align.config -o ./TEST
```

or you should submit the task to a cluster with DIVIS compiled

```
bsub -W 10000 -q c_bniu -e TEST.divis_align.err -o TEST.divis_align.out 'divis substep -s align -c ./TEST.align.config -o ./TEST'
```

An example of DIVIS pipeline "wes_somatic": 

```
bsub -W 10000 -q c_bniu -e TEST.divis_align.err -o TEST.divis_align.out 'divis substep -s align -c ./TEST.align.config -o ./TEST'
```

You can preview  the details of a substep or pipeline command with -p/--preview 

```
 [1] /bin/bwa mem -t 8 -M -R "@RG\tID:TEST\tLB:TEST\tSM:TEST\tPL:Illumina" ucsc.hg19.fasta TEST.1.fastq.gz TEST.2.fastq.gz | samtools view -Shb -o TEST.bwa.bam -
 [2] java -jar /bin/picard.jar SortSam INPUT=TEST.bwa.bam OUTPUT=TEST.sort.bam SORT_ORDER=coordinate TMP_DIR=TEST.picard.tmp
 [3] java -jar /bin/picard.jar MarkDuplicates INPUT=TEST.sort.bam OUTPUT=TEST.dedupped.bam METRICS_FILE=TEST.dedupped.metrics VALIDATION_STRINGENCY=STRICT CREATE_INDEX=true REMOVE_DUPLICATES=true TMP_DIR=TEST.picard.tmp
 [4] java -jar /bin/gatk3/GenomeAnalysisTK.jar -T RealignerTargetCreator -R ucsc.hg19.fasta -I TEST.dedupped.bam -o TEST.realigner.intervals -known 1000G_phase1.indels.hg19.sites.vcf -known Mills_and_1000G_gold_standard.indels.hg19.sites.vcf --intervals S07604514_Padded.bed
 [5] java -jar /bin/gatk3/GenomeAnalysisTK.jar -T IndelRealigner -R ucsc.hg19.fasta -I TEST.dedupped.bam -targetIntervals TEST.realigner.intervals -o TEST.realigned.bam -known 1000G_phase1.indels.hg19.sites.vcf -known Mills_and_1000G_gold_standard.indels.hg19.sites.vcf --intervals S07604514_Padded.bed
 [6] /bin/gatk4/gatk BaseRecalibrator -R ucsc.hg19.fasta -I TEST.realigned.bam -O TEST.baserecal.grp --known-sites 1000G_phase1.indels.hg19.sites.vcf --known-sites Mills_and_1000G_gold_standard.indels.hg19.sites.vcf --intervals S07604514_Padded.bed
 [7] /bin/gatk4/gatk ApplyBQSR -R ucsc.hg19.fasta -I TEST.realigned.bam --bqsr-recal-file TEST.baserecal.grp -O TEST.bqsr.bam
```

## Output 

DIVIS creates an output directory under the user specified output directory (-o/--out_dir) according to the parameters specified by -s/--step or -f/--worklflow. An example output of a test sample: 

```
drwxrwxr-x 2 scuser scuser 4096 Jan 13 10:10 qc_to_align
-rw-rw-r-- 1 scuser scuser 1547 Jan 13 10:10 qc_to_align.macros
drwxrwxr-x 2 scuser scuser 4096 Jan 15 21:49 varscan_somatic
-rw-rw-r-- 1 scuser scuser 1600 Jan 15 19:44 varscan_somatic.macros
drwxrwxr-x 2 scuser scuser 4096 Jan 17 16:06 vardict_somatic
-rw-rw-r-- 1 scuser scuser 1042 Jan 17 13:48 vardict_somatic.macros
drwxrwxr-x 3 scuser scuser 4096 Jan 18 11:32 strelka_somatic
-rw-rw-r-- 1 scuser scuser  737 Jan 18 09:24 strelka_somatic.macros
drwxrwxr-x 2 scuser scuser 4096 Jan 20 11:05 pindel_somatic
-rw-rw-r-- 1 scuser scuser 1096 Jan 20 11:05 pindel_somatic.macros
drwxrwxr-x 3 scuser scuser 4096 Jan 21 08:53 divis_report
-rw-rw-r-- 1 scuser scuser 300  Jan 21 08:53 divis_report.macros
```

 DIVIS saves all intermediate and final results, for example: 

```
$ ll divis_report/
total 5440
-rw-rw-r-- 1 scuser scuser 5199014 Feb 19  2013 TEST.funcotated.maf
-rw-rw-r-- 1 scuser scuser  262946 Feb 19  2013 TEST.merged.vcf
-rw-rw-r-- 1 scuser scuser   27369 Feb 19  2013 TEST.merged.vcf.idx
-rw-rw-r-- 1 scuser scuser    3004 Feb 19  2013 divis_gather_annotation_info.pl
-rw-rw-r-- 1 scuser scuser    2061 Feb 19  2013 divis_gather_mutations_of_callers.pl
-rw-rw-r-- 1 scuser scuser    2394 Feb 19  2013 divis_report.command.log
-rw-rw-r-- 1 scuser scuser   37715 Feb 19  2013 divis_report.err
-rw-rw-r-- 1 scuser scuser      54 Feb 19  2013 divis_report.ok.log
-rw-rw-r-- 1 scuser scuser      49 Feb 19  2013 divis_report.out
-rw-rw-r-- 1 scuser scuser   32087 Feb 19  2013 divis_report.py
-rw-rw-r-- 1 scuser scuser    2176 Feb 19  2013 flow.json
-rw-rw-r-- 1 scuser scuser     220 Feb 19  2013 mutation_of_callers.txt
drwxrwxr-x 3 scuser scuser    4096 Feb 19  2013 release
```

- **Description of universal output (program running status related):** 

1. ***[output_dir].command.log*** :  all executed command lines

2. ***[output_dir].ok.log*** : successful executed command lines;  Important during backtracking when GPyFlow-CLI is not running properly

3. ***[output_dir].out*** :  redirects standard output

4. ***[output_dir].err***: redirects standard error

   

- **Description of DIVIS internal scripts:** 

  DIVIS contains post-processing scripts (names begin with "*divis-*")for some software to add labels, merge mutations, statistics, etc. These files are free to edit to meet your specific needs. Examples of DIVIS internal scripts: 

  ```
  divis_dbsnp_filter.pl
  divis_generate_dbsnp_filter_config.pl
  divis_generate_fpfilter_config.pl
  divis_generate_strelka_config.py
  divis_process_strelka_indel_vcf.pl
  divis_process_strelka_snv_vcf.pl
  divis_snv_filter.pl
  ```

  

- **Decription of genome sequencing analysis results:**

  DIVIS saves all the intermediate results. In order to distinguish the relationship between the files,analysis output are named by its origins and meanings in a incremental manner. Such as the snv results (part) of VarScan2 :

  ```
  TEST.varscan.som_snv.vcf   ## *raw snvs of VarScan2* 
  TEST.varscan.som_snv.Somatic.vcf   ## *Somatic snvs of VarScan2*
  TEST.varscan.som_snv.Somatic.hc.vcf  ## *high confidence somatic snvs of VarScan2* 
  TEST.varscan.som_snv.Somatic.hc.somatic_pass.vcf  ## *filtered high confidence somatic snvs of VarScan2*
  ```

# Licence

DIVIS code is freely available under the [MIT license](http://www.opensource.org/licenses/mit-license.html). You can use DIVIS for free as long as for non-profit research purposes. However, if you plan to use DIVIS for commercial purposes, a licence is required and please contact hexy@cnic.cn or niubf@cnic.cn to obtain one.



# Contact 

Please contact Beifang Niu (niubf@cnic.cn)，Xiaoyu He (hexy@cnic.cn)  and Yu Zhang (polozy314@gmail.com) for any issues of DIVIS.
