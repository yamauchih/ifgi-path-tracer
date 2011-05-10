#!/bin/sh
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# run all test
#
set -e

# set the PYTHONPATH to ifgi-path-tracer/ directory
CURDIR=`pwd`
cd ../../
export PYTHONPATH=`pwd`
echo "export PYTHONPATH=${PYTHONPATH}"
cd ${CURDIR}

if [ $# -eq 0 ]; then
    # if not specified a test, test all
    for i in test_*.py
    do
        echo "running all: $i"
        python $i
    done
else
    for i in $*
    do
        echo "running arg: $i"
        python $i
    done
fi
