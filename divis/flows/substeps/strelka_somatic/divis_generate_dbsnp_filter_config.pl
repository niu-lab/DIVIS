#!/usr/bin/env perl
use strict;
use warnings;

my ($config_name,$SnpSift,$dbsnp_db,$variant_file,$mode,$dbsnp_pass_file,$dbsnp_present_file) = @ARGV;

open FF, ">$config_name";

print FF "streka.dbsnp.snv.annotator = $SnpSift\n";
print FF "streka.dbsnp.snv.db = $dbsnp_db\n";
print FF "streka.dbsnp.snv.rawvcf = $variant_file\n";
print FF "streka.dbsnp.snv.mode = $mode\n";
print FF "streka.dbsnp.snv.passfile  = $dbsnp_pass_file\n";
print FF "streka.dbsnp.snv.dbsnpfile = $dbsnp_present_file\n";

close FF;
