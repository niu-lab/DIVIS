#!/usr/bin/perl


use strict;
use warnings;
#die unless @ARGV == 6;
my ($gatk3,$sample_name,$ref_genome,$mutect_snv,$varscan_snv,$varscan_indel,$strelka_snv,$strelka_indel,$pindel)=@ARGV;

my $max_indel_size = 100;

my $pindel_vcf = $pindel;
my $sep_pos = rindex($pindel_vcf,"/"); 
my $vcf_pos = rindex($pindel_vcf,"vcf");
my $pindel_filterd_vcf = substr($pindel_vcf,$sep_pos+1,$vcf_pos)."pindel_indel_length_filtered.vcf"; 

my $cmd1 ="perl divis_filter_large_indel.pl $pindel_vcf $pindel_filterd_vcf $max_indel_size"; 
system($cmd1);

my $merge_vcf = "$sample_name.merged4.vcf";
my $cmd2="java -jar $gatk3 -R $ref_genome -T CombineVariants -o $merge_vcf --variant:varscan $varscan_snv --variant:strelka $strelka_snv --variant:mutect $mutect_snv --variant:varindel $varscan_indel --variant:sindel $strelka_indel --variant:pindel $pindel_filterd_vcf -genotypeMergeOptions PRIORITIZE -priority strelka,varscan,mutect,sindel,varindel,pindel";

system($cmd2);

1; 
