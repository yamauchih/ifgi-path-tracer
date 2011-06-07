#
# Makefile for ifgi/scene
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
	res_ray_tri_intersect.png 	\
	test_primitive.prof 		\
	test_film_result.png


#----------------------------------------------------------------------
#
# setup depends on each Makefile and TARGET
#
include $(IFGI_ROOT)/tool/Postmake.mk
