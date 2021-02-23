find -name *_D -o -name *_SI -o -name *_INV -o -name *_TD > ./pindel.out.filelist
list=$(xargs -a  ./pindel.out.filelist)
cat $list | grep ChrID > ./pindel.out.raw
