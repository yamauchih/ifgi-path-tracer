#!/bin/sh
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
# run all test

set -e

# set the PYTHONPATH to ifgi-path-tracer/ directory
CURDIR=`pwd`
cd ../../
export PYTHONPATH=`pwd`
echo "export PYTHONPATH=${PYTHONPATH}"
cd ${CURDIR}

if [ $# -eq 0 ]; then
    echo "Usage: test_one.sh test_foo.py"
    exit 1
else
    for i in $*
    do
        echo "running arg: $i"
        python $i
    done
fi
