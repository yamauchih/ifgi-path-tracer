#!/bin/sh
#
# run all test

for i in test_*.py
do
    echo "running $i"
    python $i
done
