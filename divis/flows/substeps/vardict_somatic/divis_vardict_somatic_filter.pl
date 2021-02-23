#!/usr/bin/env perl

my $infile=@ARGV[0];
map{
    chomp;
    $line=$_;
    if(/^#/){
	if(/fileformat/){
		print "##fileformat=VCFv4.3";
	}else{
        	print $line."\n";
	}
    }else{ 
        @tmp = split(/\t/,$line);
        chomp(@tmp);
	$alt_exp = $tmp[4]; 	
        @t_tmp = split(/:/,$tmp[9]);
        @n_tmp = split(/:/,$tmp[10]);
        $t_af = $t_tmp[6];
        $n_af = $n_tmp[6];
        $af_bias = ($t_af-$n_af)/($t_af+$n_af);
        $filter = $tmp[6];
        $_=~/(.*)STATUS=(\w+);(.+)DP=(\d+)(.+)AF=([\d.]+);/; 
        if(($alt_exp ne "<DEL>") && ($alt_exp ne "<INS>") &&($alt_exp ne "<DUP>") && ($filter eq "PASS") && ($2 eq "StrongLOH" || $2 eq "StrongSomatic" || $2 eq "LikelyLOH" || $2 eq "LikelySomatic" || $2 eq "AFDiff") && ($4 >= 10) && ($6 >= 0.05) && ($af_bias >=0.36)){
	    print $line."\n"
        }
    }
}`cat $infile`
