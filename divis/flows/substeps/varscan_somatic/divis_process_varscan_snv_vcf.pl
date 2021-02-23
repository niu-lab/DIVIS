#!/usr/bin/env perl

use strict;
use warnings;
use List::Util qw(sum); 

die unless @ARGV == 2;
my ($infile, $outfile, @header, $encoding, %assoc);

$infile = $ARGV[0];  $outfile = $ARGV[1];

# Insert custom info line after last existing info line, then update info
%assoc = ("VarScan"=>1,"Pindel"=>2,"Strelka"=>3,"VarDict"=>4,"MuTect1"=>5);
$encoding="VarScan,1;Pindel,2;Strelka,3;VarDict,4;MuTect1,5";
# print "The program:$ARGV[0]; is not supported now\n" and die if not exists($assoc{"$ARGV[0]"});
open (PARSE,">>","stat_vcf_mutation.txt");
open (OUT,">", $outfile) || die "Error: cannot open output file $outfile";
print OUT "##fileformat=VCFv4.0\n";
print OUT "##source=varscan\n";
print OUT "##reference=hg19\n";
print OUT "##INFO=<ID=DIVISID,Number=.,Type=Integer,Description=\"Call support from programs ".$encoding."\">\n";
print OUT "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n";
print OUT "##FORMAT=<ID=AD,Number=2,Type=Integer,Description=\"Allelic depths for the ref and alt alleles in the order listed\">\n";
print OUT "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tNORMAL\tTUMOR\n";
# chrM    15656   .       A       AT      .       PASS    DP=5720;SOMATIC;SS=2;SSC=255;GPV=1E0;SPV=0E0;GENOMEVIP=1        GT:GQ:DP:RD:AD:FREQ:DP4 0/0:.:1827:1763:3:0.17%:987,776,1,2     0/1:.:3893:1800:2023:52.92%:1733,67,1946,77

open (IN, "<", $infile) || die "Error: cannot open input file $infile"; 
my $snv_num = 0;
my $titv_ratio = 0; 
my $ti_num = 0;
my $tv_num = 0;

while(<IN>) { 
    if($_ !~ /^#/) {
	chomp; 
	my @a = split /\t/;
	# GT:GQ:DP:RD:AD:FREQ:DP4
	my @varscan_format = split(/:/,$a[8]);
	my @normal = split(/:/,$a[9]);
	my @tumor = split(/:/,$a[10]);
	my $normal_gt = $normal[0]; 
	my $tumor_gt = $tumor[0];
	my $normal_ref_depth = $normal[3];
	my $normal_alt_depth = $normal[4];
	my $tumor_ref_depth = $tumor[3];
	my $tumor_alt_depth = $tumor[4];

	$a[7] = "DIVISID=1";
	$a[8] = "GT:AD";
	$a[9] = "$normal_gt:$normal_ref_depth,$normal_alt_depth";
	$a[10] = "$tumor_gt:$tumor_ref_depth,$tumor_alt_depth";
	if(length($a[3]) <=100 && length($a[4]) <=100){	
	    print OUT join("\t", @a)."\n";
	    if(length($a[3]) == length($a[4]) && length($a[4]) ==1){ 
		$snv_num +=1;
		if(($a[3] eq "A" && $a[4] eq "G") || ($a[3] eq "G" && $a[4] eq "A") || ($a[3] eq "C" && $a[4] eq "T") || ($a[3] eq "T" && $a[4] eq "C")){ $ti_num ++; }
		if((($a[3] eq "A" || $a[3] eq "G") && ($a[4] eq "C" || $a[4] eq "T")) || (($a[3] eq "C" || $a[3] eq "T") && ($a[4] eq "A" || $a[4] eq "G"))){ $tv_num++; }
	    }
	}
    }
}
$titv_ratio = $ti_num/$tv_num;
print PARSE "VarScan_SNV:$snv_num\nVarScan_TITV:$titv_ratio\n";
close PARSE;

close(IN);
close(OUT);
