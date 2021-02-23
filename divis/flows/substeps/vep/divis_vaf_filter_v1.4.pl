#!/usr/bin/perl

## tumor >= 5% and normal <=1% 
### pindel tumor >=10% since the vaf calculation underestimate the ref coverage ##
### add the filtering for indel length ##

use strict;
use warnings;
die unless @ARGV == 7;
#my ($run_dir,$min_vaf_somatic,$min_coverage_t,$min_coverage_n,$indel_max_size)=@ARGV; 
my ($merged_vcf,$merged_filtered_vcf,$merged_out_vcf,$min_vaf_somatic,$min_coverage_t,$min_coverage_n,$indel_max_size)=@ARGV;

my $f_m=$merged_vcf; 
my $f_filter_out=$merged_filtered_vcf;
my $f_vaf_out=$merged_out_vcf;
my $max_vaf_germline=0.02; 

open(OUT1,">$f_filter_out");
open(OUT2,">$f_vaf_out"); 

foreach my $l (`cat $f_m`){
	my $ltr=$l;
	chomp($ltr);  
	if($ltr=~/^#/){print OUT1 $ltr,"\n"; next;}
	else {
		my @temp=split("\t",$ltr); 
		my $info=$temp[7];
		my @temp2; 	
		my %rc; 
		my %rc2;
		my $r_tot;  
		my $r_tot2; 
		my $vaf_n;
		my $vaf_t;
		my $ref;
		my $var;
		my $nt;
		my $ndp_ref;
		my $ndp_var;
		my $tdp_ref;
		my $tdp_var; 
		$ref=$temp[3];
		$var=$temp[4];
		
		## hexiaoyu edit: indel length filter
		if(length($ref)>$indel_max_size || length($var)>$indel_max_size){ next; }
 		
		## hexiaoyu edit here: format is " DP:DP2:DP50:FDP50:SUBDP50:TAR:TIR:TOR "
		if($info=~/set\=sindel-varindel/ || $info=~/set\=sindel-pindel/){
			$vaf_n=$temp[9];
		 	$vaf_t=$temp[10];
		 	$ref=$temp[3]; 
		 	$var=$temp[4];
		 	$r_tot=0;
		 	@temp2=split(":",$vaf_n);
			# Somatic indel allele frequency is: alt_t1count / (ref_t1count + alt_t1count)
			# alt_t1count = $alt_counts[0] (...likewise..)
			# ref_t1count = $ref_counts[0] (use the tier1 counts -- the first value in the comma-delimited list)
			# ref_counts = value of FORMAT column value TAR
			# alt_counts = value of FORMAT column value TIR
			my $rcvar=(split(",",$temp2[-2]))[0]; # TIR: Reads strongly supporting indel allele for tiers 1,2
	 	 	my $rctot=(split(",",$temp2[-3]))[0]+(split(",",$temp2[-2]))[0]; # TAR : Reads strongly supporting alternate allele for tiers 1,2
			my $rcref=$rctot-$rcvar; 
			@temp2=split(":",$vaf_t);
			my $rc2var=(split(",",$temp2[-2]))[0];
			my $rc2tot=(split(",",$temp2[-3]))[0]+(split(",",$temp2[-2]))[0];
			my $rc2ref=$rc2tot-$rc2var; 		
			
			print OUT2 $temp[0],"\t",$temp[1],"\t",$temp[2],"\t",$temp[3],"\t",$temp[4],"\t",$info,"\t",$rcref,"\t",$rcref/$rctot,"\t",$rcvar,"\t",$rcvar/$rctot,"\t",$rc2ref,"\t",$rc2ref/$rc2tot,"\t",$rc2var,"\t",$rc2var/$rc2tot,"\n"; 

			if($rc2var/$rc2tot>=$min_vaf_somatic && $rcvar/$rctot<=$max_vaf_germline && $rc2tot>=$min_coverage_t && $rctot>=$min_coverage_n){
				$ltr=~s/SVTYPE=//g;
				print OUT1 $ltr,"\n";
			} 	
		}
		## hexiaoyu edit here: format is " AU:CU:DP:FDP:GU:SDP:SUBDP:TU "
		if($info=~/set\=strelka-varscan/ || $info=~/set\=strelka-mutect/){
			$vaf_n=$temp[9];
			$vaf_t=$temp[10];
			$ref=$temp[3];
			$var=$temp[4];
			$r_tot=0;
            		@temp2=split(":",$vaf_n);
            		%rc=();
			$rc{'A'}=(split(",",$temp2[0]))[0];
			$rc{'C'}=(split(",",$temp2[1]))[0];
			$rc{'G'}=(split(",",$temp2[4]))[0];
			$rc{'T'}=(split(",",$temp2[7]))[0];
			foreach my $nt (keys %rc){
		                $r_tot+=$rc{$nt};
            		}
			@temp2=split(":",$vaf_t);
			%rc2=();
			$rc2{'A'}=(split(",",$temp2[0]))[0];
			$rc2{'C'}=(split(",",$temp2[1]))[0];
			$rc2{'G'}=(split(",",$temp2[4]))[0];
			$rc2{'T'}=(split(",",$temp2[7]))[0];
			foreach $nt (sort keys %rc2){
				$r_tot2+=$rc2{$nt};
			}
        		my @vars=split(",",$var);
        		my $rcvar=0;
        		my $rc2var=0;
        		foreach my $v (@vars){
				$rcvar+=$rc{$v};
				$rc2var+=$rc2{$v};
        		}
			print OUT2 $temp[0],"\t",$temp[1],"\t",$temp[2],"\t",$temp[3],"\t",$temp[4],"\t",$info,"\t",$rc{$ref},"\t",$rc{$ref}/$r_tot,"\t",$rcvar,"\t",$rcvar/$r_tot,"\t",$rc2{$ref},"\t",$rc2{$ref}/$r_tot2,"\t",$rc2var,"\t",$rc2var/$r_tot2,"\n";

        		if($rc2var/$r_tot2>=$min_vaf_somatic && $rcvar/$r_tot<=$max_vaf_germline && $r_tot2>=$min_coverage_t && $r_tot>=$min_coverage_n){
				print OUT1 $ltr,"\n";
			}
		}
		## FORMAT is : GT:AD:DP:DP4:FREQ:RD
		##FORMAT=<ID=DP4,Number=1,Type=String,Description="Strand read counts: ref/fwd, ref/rev, var/fwd, var/rev">
		##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
		##FORMAT=<ID=FDP,Number=1,Type=Integer,Description="Number of basecalls filtered from original read depth for tier1"> 	
		if($info=~/set\=varscan-mutect/ || $info=~/set\=varindel-sindel/ || $info=~/set\=varindel-pindel/){
			$vaf_n=$temp[9];
			$vaf_t=$temp[10];
			@temp2=split(":",$vaf_n); 
			my @ndp4=split(",",$temp2[3]);
			if(scalar @ndp4<4){@ndp4=split(",",$temp2[2]);}  
			$ndp_ref=$ndp4[0]+$ndp4[1];
			$ndp_var=$ndp4[2]+$ndp4[3];
            		
			@temp2=split(":",$vaf_t);
            		my @tdp4=split(",",$temp2[3]);
            		if(scalar @tdp4<4) { @tdp4=split(",",$temp2[2]);  }	
			$tdp_ref=$tdp4[0]+$tdp4[1];
			$tdp_var=$tdp4[2]+$tdp4[3];
			print OUT2 $temp[0],"\t",$temp[1],"\t",$temp[2],"\t",$temp[3],"\t",$temp[4],"\t",$info,"\t",$ndp_ref,"\t",$ndp_ref/($ndp_ref+$ndp_var),"\t",$ndp_var,"\t",$ndp_var/($ndp_var+$ndp_ref),"\t",$tdp_ref,"\t",$tdp_ref/($tdp_ref+$tdp_var),"\t",$tdp_var,"\t",$tdp_var/($tdp_var+$tdp_ref),"\n";  
			if($tdp_var/($tdp_var+$tdp_ref) >=$min_vaf_somatic && $ndp_var/($ndp_var+$ndp_ref)<=$max_vaf_germline && $tdp_var+$tdp_ref>=$min_coverage_t && $ndp_var+$ndp_ref>=$min_coverage_n){
				$ltr=~s/SVTYPE=//g;
				print OUT1 $ltr,"\n";
			}
		}
	}
}
