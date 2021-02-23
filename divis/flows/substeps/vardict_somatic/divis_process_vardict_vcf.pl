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
open (PARSE,">","stat_vcf_mutation.txt");
my $snv_num = 0;
my $ins_num = 0;
my $del_num = 0;
my $com_num = 0;
my $titv_ratio = 0;
my $ti_num = 0;
my $tv_num = 0;

open (OUT,">", $outfile) || die "Error: cannot open output file $outfile";
print OUT "##fileformat=VCFv4.0\n";
print OUT "##source=vardict\n";
print OUT "##reference=hg19\n";
print OUT "##INFO=<ID=DIVISID,Number=.,Type=Integer,Description=\"Call support from programs ".$encoding."\">\n";
print OUT "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n";
print OUT "##FORMAT=<ID=AD,Number=2,Type=Integer,Description=\"Allelic depths for the ref and alt alleles in the order listed\">\n";
print OUT "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tNORMAL\tTUMOR\n";

# chr1    16957   .       G       T       128     PASS    STATUS=LikelySomatic;SAMPLE=AC_WGS_10T;TYPE=SNV;DP=195;VD=19;AF=0.0974;SHIFT3=0;MSI=1.000;MSILEN=1;SSF=0.07174;SOR=2.30466;LSEQ=CCCAGGTCGGCAATGTACAT;RSEQ=AGGTCGTTGGCAATGCCGGG;GENOMEVIP=4 GT:DP:VD:ALD:RD:AD:AF:BIAS:PMEAN:PSTD:QUAL:QSTD:SBF:ODDRATIO:MQ:SN:HIAF:ADJAF:NM        0/1:112:5:1,4:68,39:107,5:0.0446:2,2:47:1:28.8:1:0.07065:6.85717:20:4:0.0377:0:1.8      0/1:195:19:4,15:119,57:176,19:0.0974:2,2:41.6:1:30.2:1:0.0002:7.74203:17:8.5:0.0944:0:1.6

open (IN, "<", $infile) || die "Error: cannot open input file $infile"; 
while(<IN>) { 
    if($_ !~ /^#/) {
	chomp; 
	my @a = split /\t/;
	$_=~/(.*)STATUS=(\w+);(.+)DP=(\d+)(.+)AF=([\d.]+);/;
	if(($a[4] ne "<DEL>") && ($a[4] ne "<INV>") && ($a[4] ne "<DUP>") && length($a[3]) <=100 && length($a[4]) <=100 && ($a[6] eq "PASS") && ($2 eq "StrongLOH" || $2 eq "StrongSomatic" || $2 eq "LikelyLOH" || $2 eq "LikelySomatic" || $2 eq "AFDiff")){
	    # GT:GQ:DP:RD:AD:FREQ:DP4
	    my @normal = split(/:/,$a[10]);
	    my @tumor = split(/:/,$a[9]);
	    my $normal_gt = $normal[0];
	    my $tumor_gt = $tumor[0];
	    my $normal_ref_depth = sum(split(/,/,$normal[4]));
	    my $normal_alt_depth = $normal[2];
	    my $tumor_ref_depth = sum(split(/,/,$tumor[4]));
 	    my $tumor_alt_depth = $tumor[2];
	    $a[7] = "DIVISID=4";
	    $a[8] = "GT:AD";
	    $a[9] = "$normal_gt:$normal_ref_depth,$normal_alt_depth";
	    $a[10] = "$tumor_gt:$tumor_ref_depth,$tumor_alt_depth";
	    print OUT join("\t", @a)."\n";
	    if(length($a[3]) == length($a[4]) && length($a[4]) ==1){
		$snv_num +=1;
		if(($a[3] eq "A" && $a[4] eq "G") || ($a[3] eq "G" && $a[4] eq "A") || ($a[3] eq "C" && $a[4] eq "T") || ($a[3] eq "T" && $a[4] eq "C")){ $ti_num ++; }
		if((($a[3] eq "A" || $a[3] eq "G") && ($a[4] eq "C" || $a[4] eq "T")) || (($a[3] eq "C" || $a[3] eq "T") && ($a[4] eq "A" || $a[4] eq "G"))){ $tv_num++; }
	    }elsif($_ =~ /TYPE=Insertion/){ $del_num ++; }
	    elsif($_ =~ /TYPE=Deletion/){ $ins_num ++; }
       	    elsif($_ =~ /TYPE=Complex/){ $com_num ++; }
	}
    }
}
$titv_ratio = $ti_num/$tv_num;
print PARSE "VarDict_SNV:$snv_num\nVarDict_INS:$ins_num\nVarDict_DEL:$del_num\nVarDict_COM:$com_num\nVarDict_TITV:$titv_ratio\n";
close(IN);
close(OUT);
