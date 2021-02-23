#!/usr/bin/perl

use warnings;
use strict;

my $input_vcf=$ARGV[0];
my $intermediate_maflite=$ARGV[1];
## transfer to maflite format

open(FH,"<$input_vcf");
open(FJ,">$intermediate_maflite");

print FJ "chr\tstart\tend\tref_allele\talt_allele\n"; 
while(<FH>){
	chomp; 
	my $chr;
	my $start;
	my $end;
	my $ref;
	my $alt;

	if(!/^#/){
		my @line_array=split(/\t/,$_);
		# CHR
		my $chr=$line_array[0];

		#multiple ALT with "/", We just remian the first alt
		my $alt_pos=index($line_array[4],"/");
		if($alt_pos!=-1){
			my @tmp=split(/\//,$line_array[4]);
			$line_array[4]=$tmp[0];
		}
		my $ref_pos=index($line_array[3],"/");
		#multiple REF with "/", We just remian the first ref
		if($ref_pos!=-1){
			my @tmp=split(/\//,$line_array[3]);
			$line_array[3]=$tmp[0];
		}
		# start and end
		if(length($line_array[3]) == length($line_array[4])){
			# for snp
			if(length($line_array[3]) == 1){
				$ref=$line_array[3];
				$start=$line_array[1];
				$end=$line_array[1];
				$alt=$line_array[4];
			}
			# for mnp
			else{
				$ref=$line_array[3];
				$alt=$line_array[4];
				$start=$line_array[1];
				$end=$line_array[1]+length($ref)-1;
			}
			if(length($ref) <=100 && length($alt) <= 100){
				print FJ "$chr\t$start\t$end\t$ref\t$alt\n";
			}
		}elsif(length($line_array[3]) > length($line_array[4])){
			$ref=substr($line_array[3],1); 
			$alt="-";
			$start=$line_array[1]+1;
			$end=$start+length($ref)-1;
			if(length($ref) <=100 && length($alt) <= 100){
				print FJ "$chr\t$start\t$end\t$ref\t$alt\n";
			}
		}else{
			$start=$line_array[1];
			$end=$start+1;;
			$ref="-";
			$alt=substr($line_array[4],1);
			if(length($ref) <=100 && length($alt) <= 100){
				print FJ "$chr\t$start\t$end\t$ref\t$alt\n";
			}
		}

	}

}
close FH;
close FJ;

