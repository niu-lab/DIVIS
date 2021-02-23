#!/usr/bin/env perl

use strict;
use warnings;

die unless @ARGV == 2;
my ($infile, $outfile, @header, $encoding, %assoc);

$infile = $ARGV[0];  $outfile = $ARGV[1];

# Insert custom info line after last existing info line, then update info
%assoc = ("VarScan"=>1,"Pindel"=>2,"Strelka"=>3,"VarDict"=>4,"MuTect1"=>5);
$encoding="VarScan,1;Pindel,2;Strelka,3;VarDict,4;MuTect1,5";
# print "The program:$ARGV[0]; is not supported now\n" and die if not exists($assoc{"$ARGV[0]"});

open (PARSE,">","stat_vcf_mutation.txt");
my $ins_num = 0;
my $del_num = 0;
my $com_num = 0;

open (OUT,">", $outfile) || die "Error: cannot open output file $outfile";
print OUT "##fileformat=VCFv4.0\n";
print OUT "##source=pindel\n";
print OUT "##reference=hg19\n";
print OUT "##INFO=<ID=DIVISID,Number=.,Type=Integer,Description=\"Call support from programs ".$encoding."\">\n";
print OUT "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n";
print OUT "##FORMAT=<ID=AD,Number=2,Type=Integer,Description=\"Allelic depths for the ref and alt alleles in the order listed\">\n";
print OUT "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tNORMAL\tTUMOR\n";
open (IN, "<", $infile) || die "Error: cannot open input file $infile"; 
while(<IN>) {
    # keep only the INS and DEL 
    if($_ !~ /^#/ && $_ !~/SVTYPE=RPL/) {
	chomp; 
	my @a = split /\t/;
	# keep the length of variant <= 100 
	if(length($a[3]) <=100 && length($a[4]) <=100){
	    $a[7] = "DIVISID=2";
	    print OUT join("\t", @a)."\n";
	    if($_ =~ /SVTYPE=DEL/){ $del_num++; }
	    elsif($_ =~ /SVTYPE=INS/){ $ins_num ++; }
	}
    }
}
print PARSE "Pindel_SNV:0\nPindel_INS:$ins_num\nPindel_DEL:$del_num\nPindel_COM:$com_num\nPindel_TITV:NA";
close(IN);
close(OUT);
