#!/bin/bash
set -e

# change to specific name
processor=$(uname -m)
target_file=libunitree_idl_${processor}.a

# all idl file
cp ../go2/idl/*.idl .
cp ../ros2/*.idl .
cp ../g1/*.idl .


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

rm -f *.cpp *.o *.idl

mkdir -p include
mv *.hpp include

mkdir -p lib
mv $target_file lib