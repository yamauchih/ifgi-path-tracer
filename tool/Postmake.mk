#
# Post-Makefile
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#

#----------------------------------------------------------------------
# if SUBDIR is defined in the Makefile, it is used (so far for clean
# only)
#
# SUBDIR :=

# for check target
TEST_ALL_SH_FILE := ./test_all.sh


#----------------------------------------------------------------------
# the following target is phony targets (always run the command)
.PHONY: all clean check

all:

clean:
	rm -rfv *.pyc *~ html/
	$(foreach subdir, $(SUBDIR),\
		$(MAKE) --directory=$(subdir) clean;)

# if test_all.sh exists, then call it.
#
# Don't use $(shell $(TEST_ALL_SH_FILE)) instead of
# $(TEST_ALL_SH_FILE) in 'if' since 'shell' command use the stdout for
# the return status and evaluate that. (I saw the weird error message
# like
#
#   export: 1: test_DrawMode.py: bad variable name
#
check:
	$(if $(wildcard $(TEST_ALL_SH_FILE)),\
		$(TEST_ALL_SH_FILE),\
		)
	$(foreach subdir, $(SUBDIR),\
		$(MAKE) --directory=$(subdir) check;)


doc:
	doxygen
