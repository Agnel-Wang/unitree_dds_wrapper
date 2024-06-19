#!/bin/bash

# all idl file
cp ../go2/idl/*.idl .
cp ../ros2/*/*.idl .
# cp ../ros2/std_msgs/*.idl .

for dir in `ls *.idl`
do
    idlc -l py -I idl $dir
done

rm -f *.idl