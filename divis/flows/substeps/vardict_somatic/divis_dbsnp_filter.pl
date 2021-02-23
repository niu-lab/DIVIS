#!/usr/bin/env perl
use strict;
use warnings;

use Cwd;
use Carp;
use FileHandle;
use IO::File;
use Getopt::Long;
use POSIX qw( WIFEXITED );
use File::Temp qw/ tempfile /;
#use File::stat;

sub checksize {
	my ($dest,$src) = @_;
	my $fs = `wc -l < $dest`;
	if ( $fs == 0){ system("grep ^# $src > $dest"); }
		return 1;
}

my (%paras);
# parse paras from config file
map{chomp; if(!/^[#;]/ && /=/){@_ = split /=/; $_[1] =~ s/ //g; my $v = $_[1]; print $v."\n"; $_[0] =~ s/ //g; $paras{(split /\./, $_[0])[-1]} = $v}}(<>);

# Use uncompressed db to avoid being bitten by java compression bug
my $anno=$paras{'rawvcf'}."dbsnp_anno.vcf";
if($paras{'rawvcf'} =~ /\.vcf$/){
	($anno = $paras{'rawvcf'}) =~ s/\.vcf$/\.dbsnp_anno\.vcf/;
}
#### ---- hexy edit -----
#my $cmd = "java $ENV{'JAVA_OPTS'} -jar $paras{'annotator'} annotate -id $paras{'db'} $paras{'rawvcf'} > $anno";
#Usage: java -jar SnpSift.jar Annotate [options] database.vcf file.vcf > newFile.vcf
#-id : Only annotate ID field (do not add INFO field). Default: true
my $cmd = "java -jar $paras{'annotator'} annotate -id $paras{'db'} $paras{'rawvcf'} > $anno"; 
print "$cmd\n";
system($cmd);

checksize($anno, $paras{'rawvcf'});

if(exists $paras{'mode'} && $paras{'mode'} eq "filter"){
	####  ---- hexy edit -----
	#$cmd = "java $ENV{'JAVA_OPTS'} -jar $paras{'annotator'} filter -n \"(exists ID) & (ID =~ 'rs')\" -f $anno > $paras{'passfile'}";
	$cmd = "java -jar $paras{'annotator'} filter -n \"(exists ID) & (ID =~ 'rs')\" -f $anno > $paras{'passfile'}";
	system($cmd);
	print $cmd."\n";
	checksize($paras{'passfile'}, $anno);
	#### ---- hexy edit -----
	#$cmd = "java $ENV{'JAVA_OPTS'} -jar $paras{'annotator'} filter \"(exists ID) & (ID =~ 'rs') \" -f $anno > $paras{'dbsnpfile'}";
	$cmd = "java -jar $paras{'annotator'} filter \"(exists ID) & (ID =~ 'rs') \" -f $anno > $paras{'dbsnpfile'}";
	system($cmd);
	print $cmd."\n";
	checksize($paras{'dbsnpfile'}, $anno);
	$cmd = "rm -f $anno";
	system($cmd);
}
1;
