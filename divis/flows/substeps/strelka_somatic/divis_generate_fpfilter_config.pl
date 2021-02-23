#!/usr/bin/env perl
use strict;
use warnings;

my ($config_name,$bam_readcount,$t_bam_file,$variant_file,$fp_pass_file,$fp_fail_file,$rc_in_file,$rc_out_file,$fp_out_file,$ref) = @ARGV;

open FF, ">$config_name";

print FF "fpfilter.snv.bam_readcount = $bam_readcount\n";
print FF "fpfilter.snv.bam_file = $t_bam_file\n";
print FF "fpfilter.snv.REF = $ref\n";
print FF "fpfilter.snv.variants_file = $variant_file\n";
print FF "fpfilter.snv.passfile = $fp_pass_file\n";
print FF "fpfilter.snv.failfile = $fp_fail_file\n";
print FF "fpfilter.snv.rc_in = $rc_in_file\n";
print FF "fpfilter.snv.rc_out = $rc_out_file\n";
print FF "fpfilter.snv.fp_out = $fp_out_file\n";
print FF "fpfilter.snv.min_mapping_qual = 0\n";
print FF "fpfilter.snv.min_base_qual = 15\n";
print FF "fpfilter.snv.min_num_var_supporting_reads = 4\n";
print FF "fpfilter.snv.min_var_allele_freq = 0.05\n";
print FF "fpfilter.snv.min_avg_rel_read_position = 0.10\n";
print FF "fpfilter.snv.min_avg_rel_dist_to_3prime_end = 0.10\n";
print FF "fpfilter.snv.min_var_strandedness = 0.01\n";
print FF "fpfilter.snv.min_allele_depth_for_testing_strandedness = 5\n";
print FF "fpfilter.snv.min_ref_allele_avg_base_qual = 30\n";
print FF "fpfilter.snv.min_var_allele_avg_base_qual = 30\n";
print FF "fpfilter.snv.max_rel_read_length_difference = 0.25\n";
print FF "fpfilter.snv.max_mismatch_qual_sum_for_var_reads = 150\n";
print FF "fpfilter.snv.max_avg_mismatch_qual_sum_difference = 150\n";
print FF "fpfilter.snv.min_ref_allele_avg_mapping_qual = 30\n";
print FF "fpfilter.snv.min_var_allele_avg_mapping_qual = 30\n";
print FF "fpfilter.snv.max_avg_mapping_qual_difference = 50\n";

close FF;
