my $in_file=@ARGV[0];
my $out_file=@ARGV[1];
open(FH, ">$out_file") or die $!;
map{
    chomp;
    @list=split(/\t/,$_);
    $col_ref=length($list[2]);
    $col_alt=length($list[3]);
    if($col_ref==$col_alt){
        $start=$stop=$list[1];
        print FH "$list[0]\t$start\t$stop\n";
    }else{
        $indel_size=$col_ref>$col_alt?$col_ref:$col_alt;
        $indel_start=$list[1];
        $indel_stop=$indel_start+$indel_size;
        $start=$indel_start-$indel_size-1;
        $stop=$indel_stop+$indel_size+1;
        $chr_id=$list[0];
        print FH "$list[0]\t$start\t$stop\n";
     }
}`cat $in_file`;
close FH;