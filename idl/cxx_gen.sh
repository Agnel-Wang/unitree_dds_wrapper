#!/bin/bash
set -e

# change to specific name
target_file=libcustom_idl_cpp.a

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

rm -f *.cpp *.o

mkdir -p include
mv *.hpp include

mkdir -p lib
mv $target_file lib