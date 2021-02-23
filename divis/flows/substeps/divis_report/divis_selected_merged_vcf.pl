#!/usr/bin/env perl

use warnings;
use strict;

my $infile = $ARGV[0];
my $out_file = $ARGV[1];

open MERGED, "<$infile";
open SELECTED, ">$out_file";

while(<MERGED>){
    chomp();
    if(/^#/){print SELECTED $_."\n";}
    else{
	$_ =~ /(.*)set=([\w-]+)\s/;
	if(index($2,"-") > 0){
	    print SELECTED $_."\n";
	}	
    }
}

close MERGED;
close SELECTED;
