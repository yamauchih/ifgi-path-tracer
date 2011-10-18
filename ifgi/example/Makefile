#
# Makefile for ifgi/render
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

# root directory of ifgi-path-tracer
IFGI_ROOT := ../..

#
# common setup/defines
#
include $(IFGI_ROOT)/tool/Premake.mk

#----------------------------------------------------------------------
# each Makefile define
#----------------------------------------------------------------------
# sub directories
SUBDIR :=

# additional clean files
ADDITIONAL_CLEAN_FILE := 		\
	test_ifgi_render_0.Hit.png	\
	test_ifgi_render_1.Hit.png	\
	test_ifgi_render_1.RGBA.png	\
	test_ifgi_render_1.Zbuf.png	\


#----------------------------------------------------------------------
#
# setup depends on each Makefile and TARGET
#
include $(IFGI_ROOT)/tool/Postmake.mk
