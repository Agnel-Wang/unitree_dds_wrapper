#!/bin/bash
processor=$(uname -m)

cp -r include/unitree/* /usr/local/include/unitree
cp lib/${processor}/libunitree_idl.a /usr/local/lib
