#!/usr/bin/env perl
use strict;
use warnings;

my ($config_name,$SnpSift,$dbsnp_db,$variant_file,$mode,$dbsnp_pass_file,$dbsnp_present_file) = @ARGV;

open FF, ">$config_name";

print FF "dbsnp.annotator = $SnpSift\n";
print FF "dbsnp.db = $dbsnp_db\n";
print FF "dbsnp.rawvcf = $variant_file\n";
print FF "dbsnp.mode = $mode\n";
print FF "dbsnp.passfile  = $dbsnp_pass_file\n";
print FF "dbsnp.dbsnpfile = $dbsnp_present_file\n";

close FF;
