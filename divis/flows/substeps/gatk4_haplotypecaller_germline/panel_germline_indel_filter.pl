my $infile=@ARGV[0];
my $results_file=@ARGV[1];

open VCF,"<","$infile"; 
open PASS, ">","$results_file";
while(<VCF>){
    if(/^#/){
        print PASS $_
    }else{
        chomp; 
        @aa=split(/\t/,$_); 
        @format=split(":",$aa[9]); 
        if(@format==1){
            print PASS $_."\n"
        }elsif(@format==3){
            $gq=$format[1];
            if($gq >= 20){
                print PASS $_."\n";
            }
        }elsif(@format == 5){
            $gq=$format[3]; 
            $ad=$format[1]; 
            @freq_array=split(/,/,$ad); 
            $freq=$freq_array[1]/($freq_array[1]+$freq_array[0]); 
            if($gq >=20 && $freq>=0.1){
                print PASS $_."\n"
            }
        }
    }
}; 
close PASS;
close VCF;