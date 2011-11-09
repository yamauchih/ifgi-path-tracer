#
# root Makefile
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

# root directory of ifgi-path-tracer
IFGI_ROOT := .

#
# common setup/defines
#
include $(IFGI_ROOT)/tool/Premake.mk

#----------------------------------------------------------------------
# each Makefile define
#----------------------------------------------------------------------
SUBDIR := ifgi examiner00 examiner



#----------------------------------------------------------------------
#
# setup depends on each Makefile and TARGET
#
include $(IFGI_ROOT)/tool/Postmake.mk
