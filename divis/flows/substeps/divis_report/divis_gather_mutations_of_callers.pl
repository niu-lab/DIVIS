#!/usr/bin/env perl

use warnings;
use strict;

open MUT,">mutation_of_callers.txt";
print MUT "caller\tSNVs\tInsertions\tDeletions\tComplex\tTi/Tv\n";

my %varscan_mut_hash=();
open VS, "<../varscan_somatic/stat_vcf_mutation.txt";
while(<VS>){
    my @a=split(/:/,$_); 
    chomp(@a);
    $varscan_mut_hash{$a[0]} = $a[1];
}
close VS;

my %strelka_mut_hash = ();
open ST, "<../strelka_somatic/stat_vcf_mutation.txt";
while(<ST>){
    my @a=split(/:/,$_);
    chomp(@a);
    $strelka_mut_hash{$a[0]} = $a[1];
}
close ST;

my %vardict_mut_hash = ();
open VD, "<../vardict_somatic/stat_vcf_mutation.txt";
while(<VD>){
    my @a=split(/:/,$_);
    chomp(@a);
    $vardict_mut_hash{$a[0]} = $a[1];
}
close VD;

my %pindel_mut_hash = ();
open PI, "<../pindel_somatic/stat_vcf_mutation.txt";
while(<PI>){
    my @a=split(/:/,$_);
    chomp(@a);
    $pindel_mut_hash{$a[0]} = $a[1];
}
close PI;

my %divis_mut_hash = ();
open DIVIS, "<../divis_report/stat_vcf_mutation.txt";
while(<DIVIS>){
    if(!/^#/){
	my @a=split(/:/,$_);
	chomp(@a);
	$divis_mut_hash{$a[0]} = $a[1];
    }
}
print MUT "VarScan(v2.4.9)\t$varscan_mut_hash{'VarScan_SNV'}\t$varscan_mut_hash{'VarScan_INS'}\t$varscan_mut_hash{'VarScan_DEL'}\t$varscan_mut_hash{'VarScan_COM'}\t$varscan_mut_hash{'VarScan_TITV'}\n";
print MUT "VarDict(v1.8.7)\t$vardict_mut_hash{'VarDict_SNV'}\t$vardict_mut_hash{'VarDict_INS'}\t$vardict_mut_hash{'VarDict_DEL'}\t$vardict_mut_hash{'VarDict_COM'}\t$vardict_mut_hash{'VarDict_TITV'}\n";
print MUT "Strelka2(v0.0.3)\t$strelka_mut_hash{'Strelka_INS'}\t$strelka_mut_hash{'Strelka_INS'}\t$strelka_mut_hash{'Strelka_DEL'}\t$strelka_mut_hash{'Strelka_COM'}\t$strelka_mut_hash{'Strelka_TITV'}\n";
print MUT "Pindel(v1.1.1)\t$pindel_mut_hash{'Pindel_SNV'}\t$pindel_mut_hash{'Pindel_INS'}\t$pindel_mut_hash{'Pindel_DEL'}\t$pindel_mut_hash{'Pindel_COM'}\t$pindel_mut_hash{'Pindel_TITV'}\n";
print MUT "DIVIS(v1.0)\t$divis_mut_hash{'DIVIS_SNV'}\t$divis_mut_hash{'DIVIS_INS'}\t$divis_mut_hash{'DIVIS_DEL'}\t$divis_mut_hash{'DIVIS_COM'}\t$divis_mut_hash{'DIVIS_TITV'}\n";
close MUT;
