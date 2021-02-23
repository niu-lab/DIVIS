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
my $ins_num = 0;
my $del_num = 0;
my $com_num = 0;
open (PARSE,">>","stat_vcf_mutation.txt");

open (OUT,">", $outfile) || die "Error: cannot open output file $outfile";
print OUT "##fileformat=VCFv4.0\n";
print OUT "##source=strelka\n";
print OUT "##reference=hg19\n";
print OUT "##INFO=<ID=DIVISID,Number=.,Type=Integer,Description=\"Call support from programs ".$encoding."\">\n";
print OUT "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n";
print OUT "##FORMAT=<ID=AD,Number=2,Type=Integer,Description=\"Allelic depths for the ref and alt alleles in the order listed\">\n";
print OUT "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tNORMAL\tTUMOR\n";
# chr1    70858900        .       CT      C       .       PASS    IC=2;IHP=3;NT=ref;QSI=33;QSI_NT=33;RC=3;RU=T;SGT=ref->het;SOMATIC;TQSI=1;TQSI_NT=1;GENOMEVIP=3  DP:DP2:TAR:TIR:TOR:DP50:FDP50:SUBDP50   20:20:20,20:0,0:0,0:20.51:0.95:0.00        51:51:24,24:21,21:6,6:45.36:0.30:0.00
open (IN, "<", $infile) || die "Error: cannot open input file $infile"; 
while(<IN>) { 
    if($_ !~ /^#/) {
	chomp; 
	my @a = split /\t/;
	# DP:DP2:TAR:TIR:TOR:DP50:FDP50:SUBDP50
	# 20:20:20,20:0,0:0,0:20.51:0.95:0.00
	# 51:51:24,24:21,21:6,6:45.36:0.30:0.00
	my @strelka_format = split(/:/,$a[8]);
	my @normal = split(/:/,$a[9]);
	my @tumor = split(/:/,$a[10]);
	
	my $normal_dp = int(($normal[0] + $normal[1])/2);
	my $tumor_dp = int(($tumor[0] + $tumor[1])/2);
	my $normal_ref_depth = int(sum(split(/,/,$normal[2]))/2);
	my $normal_alt_depth = int(sum(split(/,/,$normal[3]))/2);
	my $tumor_ref_depth = int(sum(split(/,/,$tumor[2]))/2);
	my $tumor_alt_depth = int(sum(split(/,/,$tumor[3]))/2);

	my $normal_gt = "0/0";
	my $tumor_gt = "0/1";
        
	if($normal_dp > 0 && $normal_alt_depth/$normal_dp > 0.05) {$normal_gt = "0/1"; }
	if($tumor_dp > 0 && $tumor_alt_depth/$tumor_dp < 0.05) {$tumor_gt = "0/0"; }

	$a[7] = "DIVISID=3";
	$a[8] = "GT:AD";
	$a[9] = "$normal_gt:$normal_ref_depth,$normal_alt_depth";
	$a[10] = "$tumor_gt:$tumor_ref_depth,$tumor_alt_depth";
	
	if(length($a[3]) <=100 && length($a[4]) <=100){
	    print OUT join("\t", @a)."\n";
	    if((length($a[3]) > length($a[4])) && (substr($a[3],0,1) eq $a[4])){ $ins_num ++; }
	    elsif((length($a[4]) > length($a[3])) && (substr($a[4],0,1) eq $a[3])){ $del_num ++; }
	    else{$com_num ++;}
	}
    }
}

print PARSE "Strelka_INS:$ins_num\nStrelka_DEL:$del_num\nStrelka_COM:$com_num\n";
close(IN);
close(OUT);
close(PARSE);

