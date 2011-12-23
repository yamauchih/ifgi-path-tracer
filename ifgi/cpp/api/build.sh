#! /bin/sh -x
#
# Copyright (C) 2011 Hitoshi Yamauchi
#
PYTHON_INCLUDE=`python-config --includes`
MOD_CPP_SOURCE_BASE=ifgi_cpp_render_mod

g++ ${PYTHON_INCLUDE} -DPIC -shared -fPIC ${MOD_CPP_SOURCE_BASE}.cpp -o ${MOD_CPP_SOURCE_BASE}.so -lboost_python

