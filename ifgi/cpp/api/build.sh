#! /bin/sh -x
#
# Copyright (C) 2011 Hitoshi Yamauchi
#
PYTHON_INCLUDE=`python-config --includes`
MOD_CPP_SOURCE_BASE=ifgi_cpp_render_mod

# linking order is important
g++ -DPIC -shared -fPIC -o ${MOD_CPP_SOURCE_BASE}.so Ubuntu11.10/${MOD_CPP_SOURCE_BASE}.o ../base/Ubuntu11.10/libcpp_base.so -lboost_python
