#!/usr/bin/env perl

use warnings;
use strict;

my $input_merged_maf = $ARGV[0];
my $output_snv_venn_intersect = "snv_intersect.txt";
my $output_indel_venn_intersect = "indel_intersect.txt";
my $output_variant_classification_gauge = "variant_classification_gauge.txt";
my $output_variant_type_pie = "variant_type_pie.txt";
my $output_gene_tagcloud = "gene_tagcloud.txt";
my $output_chromosome_bar = "chromosome_bar.txt";

open MERGE,"<$input_merged_maf " || die "Error: cannot open input file $input_merged_maf ";
open SNVVENN, ">$output_snv_venn_intersect " || die "Error: cannot open input file $output_snv_venn_intersect ";
open INDELVENN,">$output_indel_venn_intersect " || die "Error: cannot open input file $output_indel_venn_intersect ";
open CLASS, ">$output_variant_classification_gauge " || die "Error: cannot open input file $output_variant_classification_gauge ";
open TYPE, ">$output_variant_type_pie " || die "Error: cannot open input file $output_variant_type_pie ";
open TAGCLOUD, ">$output_gene_tagcloud " || die "Error: cannot open input file $output_gene_tagcloud ";
open CHRBAR, ">$output_chromosome_bar " || die "Error: cannot open input file $output_chromosome_bar ";

my %snv_venn = ();
my %indel_venn = ();
my %variant_classification = ();
my %variant_type = ();
my %genes = ();
my %chromosome_snv = ();
my %chromosome_indel = ();
my @tmp = ();
my $chr_pre = "chr";
my $chr_name = "";
while(<MERGE>){
    if(($_ !~ /^#/) && ($_ !~ /^Hugo/)){
	@tmp = split(/\t/,$_);
	chomp(@tmp);
	$variant_classification{$tmp[8]}++;
	$variant_type{$tmp[9]}++;
	$genes{$tmp[0]}++;
	$chr_name = $chr_pre.$tmp[4];
	if($tmp[9] eq 'SNP'){
	    $snv_venn{$tmp[277]}++;
	    $chromosome_snv{$chr_name}++;
	}
	if($tmp[9] eq 'INS' || $tmp[9] eq 'DEL'){
	    $indel_venn{$tmp[277]}++; 
	    $chromosome_indel{$chr_name}++;
	}	
    }
}

my $key = ""; 
my $value = "";

foreach $key (sort{$variant_classification{$a} <=> $variant_classification{$b}} keys %variant_classification ){
    if($key ne "COULD_NOT_DETERMINE"){
        print CLASS "$key\t$variant_classification{$key}\n";
    }
}

foreach $key (sort{$variant_type{$a} <=> $variant_type{$b}} keys %variant_type ){
    print TYPE "$key\t$variant_type{$key}\n";
}

my $num = 1; 
foreach $key (sort{$genes{$b} <=> $genes{$a}} keys %genes){
    if($key ne "Unknown" && $key ne ""){
    	if($num <= 100){
	    print TAGCLOUD "$key\t$genes{$key}\n";
	    $num ++;
	}
    }
}

while(($key, $value) = each %snv_venn ){
    print SNVVENN "$key\t$value\n";
}

while(($key, $value) = each %indel_venn ){
    print INDELVENN "$key\t$value\n";
}

my @chr = ('chr1',"chr2",'chr3','chr4','chr5','chr6',"chr7",'chr8','chr9','chr10','chr11',"chr12",'chr13','chr14','chr15','chr16',"chr17",'chr18','chr19','chr20','chr21',"chr22",'chrX','chrY');
while(@chr){
    chomp;
    my $aa = shift(@chr); 
    print CHRBAR "$aa\t$chromosome_snv{$aa}\t$chromosome_indel{$aa}\n";   
}

close MERGE;
close SNV;
close INDEL;
close CLASS;
close TYPE;
close TAGCLOUD;
close CHRBAR;
