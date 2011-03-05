#!/bin/sh
#
# run all test

set -e

# set the PYTHONPATH to ifgi-path-tracer/ directory
CURDIR=`pwd`
cd ../
export PYTHONPATH=`pwd`
echo "export PYTHONPATH=${PYTHONPATH}"
cd ${CURDIR}

# test all
for i in test_*.py
do
    echo "running $i"
    python $i
done
