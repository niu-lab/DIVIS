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
open (PARSE,">>","stat_vcf_mutation.txt");
open (OUT,">", $outfile) || die "Error: cannot open output file $outfile";
print OUT "##fileformat=VCFv4.0\n";
print OUT "##source=strelka\n";
print OUT "##reference=hg19\n";
print OUT "##INFO=<ID=DIVISID,Number=.,Type=Integer,Description=\"Call support from programs ".$encoding."\">\n";
print OUT "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n";
print OUT "##FORMAT=<ID=AD,Number=2,Type=Integer,Description=\"Allelic depths for the ref and alt alleles in the order listed\">\n";
print OUT "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tNORMAL\tTUMOR\n";
my $ti_num = 0;
my $tv_num = 0;
my $titv_ratio = 0;
my $snv_num = 0;
open (IN, "<", $infile) || die "Error: cannot open input file $infile"; 
while(<IN>){ 
    if($_ !~ /^#/){
	chomp; 
	my @a = split /\t/;
	my @strelka_format = split(/:/,$a[8]);
	my @normal = split(/:/,$a[9]);
	my @tumor = split(/:/,$a[10]);
	my $normal_dp = $normal[0]; 
	my $tumor_dp = $tumor[0];
	
	my %normal_format;
	my %tumor_format;
	my $normal_ref_depth = 0;
	my $normal_alt_depth = 0;
	my $tumor_ref_depth = 0;
	my $tumor_alt_depth = 0;
	my $normal_gt = "0/0";
	my $tumor_gt = "0/1";
        
	for(my $i = 0; $i < scalar(@strelka_format); $i++){
	    $normal_format{$strelka_format[$i]} = $normal[$i];
	    $tumor_format{$strelka_format[$i]} = $tumor[$i];
	}
	my $ref_comma = index($a[3],",");
	my $alt_comma = index($a[4],",");
	if($ref_comma > 0){$a[3]=substr($a[3],0,$ref_comma);}
	if($alt_comma > 0){$a[4]=substr($a[4],0,$alt_comma);}
        my $ref_key = $a[3]."U";
        my $alt_key = $a[4]."U";
        my @normal_ref_depth_inline = split(/,/,$normal_format{$ref_key});
	my @normal_alt_depth_inline = split(/,/,$normal_format{$alt_key});
	my @tumor_ref_depth_inline = split(/,/,$tumor_format{$ref_key});
	my @tumor_alt_depth_inline = split(/,/,$tumor_format{$alt_key});
	$normal_ref_depth = int(sum(@normal_ref_depth_inline)/2);
	$normal_alt_depth = int(sum(@normal_alt_depth_inline)/2);
	$tumor_ref_depth = int(sum(@tumor_ref_depth_inline)/2); 
	$tumor_alt_depth = int(sum(@tumor_alt_depth_inline)/2);	

	if($normal_dp > 0 && $normal_alt_depth/$normal_dp > 0.05) {$normal_gt = "0/1"; }
	if($tumor_dp > 0 && $tumor_alt_depth/$tumor_dp < 0.05) {$tumor_gt = "0/0"; }

	$a[7] = "DIVISID=3";
	$a[8] = "GT:AD";
	$a[9] = "$normal_gt:$normal_ref_depth,$normal_alt_depth";
	$a[10] = "$tumor_gt:$tumor_ref_depth,$tumor_alt_depth";
	if(length($a[3]) <=100 && length($a[4]) <=100){
	    print OUT join("\t", @a)."\n";
	    if(length($a[3]) == length($a[4]) && length($a[4]) ==1){
                $snv_num +=1;
                if(($a[3] eq "A" && $a[4] eq "G") || ($a[3] eq "G" && $a[4] eq "A") || ($a[3] eq "C" && $a[4] eq "T") || ($a[3] eq "T" && $a[4] eq "C")){$ti_num ++;}
                if((($a[3] eq "A" || $a[3] eq "G") && ($a[4] eq "C" || $a[4] eq "T")) || (($a[3] eq "C" || $a[3] eq "T") && ($a[4] eq "A" || $a[4] eq "G"))){$tv_num++;} 
	    }
        }
    }
}
$titv_ratio = $ti_num/$tv_num;

print PARSE "Strella_SNV:$snv_num\nStrelka_TITV:$titv_ratio\n";
close(IN);
close(OUT);
