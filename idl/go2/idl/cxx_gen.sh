#!/bin/bash
set -e

target_file=libunitree_go2_idl_cpp.a

target_inc_dir=/usr/local/include/unitree
target_lib_dir=/usr/local/lib


ls *.idl | while read NAME
do
	/usr/local/bin/idlc -I. -l cxx $NAME 2>/dev/null
done

ls *.cpp | while read NAME
do
	echo $NAME
	g++ -Wall -fPIC -c $NAME -I/usr/local/include/ddscxx -I/usr/local/include/iceoryx/v2.0.2
done

ar -r $target_file *.o

if [ -f $target_file ]; then
   echo "generate target file success"
else
   echo "error"
fi

mkdir -p $target_inc_dir/go2_idl
mv *.hpp $target_inc_dir/go2_idl

mv $target_file $target_lib_dir
# rm -f *.cpp *.o
