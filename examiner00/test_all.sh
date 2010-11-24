#!/bin/sh
#
# run all test

set -e

for i in test_*.py
do
    echo "running $i"
    python $i
done
