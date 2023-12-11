idl_path=$1
for dir in `ls $idl_path/*.idl`
do
    idlc -l py -I $idl_path $dir
done