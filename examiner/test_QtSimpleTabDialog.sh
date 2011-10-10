#!/bin/sh
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
# run QtSimpleTabDialog.py

set -e

# set the PYTHONPATH to ifgi-path-tracer/ directory
CURDIR=`pwd`
cd ../
export PYTHONPATH=`pwd`
echo "export PYTHONPATH=${PYTHONPATH}"
cd ${CURDIR}

python QtSimpleTabDialog.py

