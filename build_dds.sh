idl_path=$1/go2/idl
for dir in `ls $idl_path/*.idl`
do
    idlc -l py -I $idl_path $dir
done