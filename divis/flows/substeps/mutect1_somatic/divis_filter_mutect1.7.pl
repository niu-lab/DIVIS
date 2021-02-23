#!/usr/bin/perl
#
### tumor >= 5% and normal <=2%
#### mutect1.7 filtering ###

use strict;
use warnings;
die unless @ARGV == 7;

my ($n_bam_SM,$t_bam_SM,$f_m,$f_filter_out,$mincov_t,$mincov_n,$minvaf)=@ARGV;

my $min_vaf_somatic=$minvaf;
my $max_vaf_germline=0.02;

open(IN,"<$f_m");
open(OUT,">$f_filter_out");

# the tumor and mormal order in Mutect1.1.7 is randomly 
my $f_bam_n=$n_bam_SM;
my $f_bam_t=$t_bam_SM;
my $tumor_normal_order=-1;

#foreach my $l (`$samtools view -H $f_bam_n`){
#	my $ltr=$l;
#	chomp($ltr);
#	if($ltr=~/^\@RG/) {
#		my @temp2=split("\t",$ltr);
#		for(my $i=0;$i<scalar @temp2;$i++){
#			if($temp2[$i]=~/^SM/){
#				$sn_n=(split(/\:/,$temp2[$i]))[1];
#				last;
#			}	
#        	}
#    	}
#}

#foreach my $l (`$samtools view -H $f_bam_t`){
#	my $ltr=$l;
#	chomp($ltr);
#	if($ltr=~/^\@RG/) {
#		my @temp2=split("\t",$ltr);
#		for(my $i=0;$i<scalar @temp2;$i++){
#			if($temp2[$i]=~/^SM/){
#				$sn_t=(split(/\:/,$temp2[$i]))[1];
#				last;
#			}
#		}
#	}
#}

while(<IN>)
{
	my $l=$_;
	chomp($l);
	if($l=~/^#/) {
		if($l=~/^#CHROM/) {
			my @temphead=split("\t",$l);
			print OUT $temphead[0];
			for(my $i=1;$i<=8;$i++){
	        	        print OUT "\t",$temphead[$i];
                	}
			# here we make the order is "NORMAL" then "TUMOR". make it consistent with VarScan/Strelka/Pindel
			if($temphead[9] eq $t_bam_SM && $temphead[10] eq $n_bam_SM){$tumor_normal_order=1;};
                	if($temphead[9] eq $n_bam_SM && $temphead[10] eq $t_bam_SM){$tumor_normal_order=0;};
			print OUT "\t","NORMAL","\t","TUMOR","\n";
		}else{ print OUT $l,"\n";}
	}else{
		if($tumor_normal_order==-1) { last; }
		my @temp=split("\t",$l);
		my $tumor=$temp[9]; 
		my $normal=$temp[10];
		
		if($tumor_normal_order==1){$tumor=$temp[9]; $normal=$temp[10];}
		elsif($tumor_normal_order==0){$normal=$temp[9]; $tumor=$temp[10];};
		#print "$tumor\t$normal\n";

		my @tempt=split(":",$tumor);
                my @tempn=split(":",$normal);
                my @readt=split(",",$tempt[1]);
                my @readn=split(",",$tempn[1]);

		my $tot_n=$readn[0]+$readn[1];
		my $tot_t=$readt[0]+$readt[1];
		
		if($tot_n==0 || $tot_t==0) { next; }
		my $vaf_t=$readt[1]/$tot_t;
		my $vaf_n=$readn[1]/$tot_n;
	
		if($temp[6] eq "PASS" && $vaf_t>=$min_vaf_somatic && $vaf_n<=$max_vaf_germline && $tot_n>=$mincov_n && $tot_t>=$mincov_t){
			if($tumor_normal_order==1){
				my @tmp=split("\t",$l);
				print OUT $tmp[0];
				for(my $j=1; $j<=8; $j++)
				{
					print OUT "\t",$tmp[$j];
				}
				print OUT "\t",$tmp[10],"\t",$tmp[9],"\n";
			}elsif($tumor_normal_order==0){
				print OUT $l,"\n";
			}
		}
	}
}
close IN;
close OUT;
