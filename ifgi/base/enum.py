#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
#
class Enum(list):
    """Enum emulation class.
    This is a list. set is more efficient, but it does not keep the
    initialization order."""
    def __getattr__(self, _name):
        if _name in self:
            return _name
        raise AttributeError

# Usage:
# Animals = Enum(["DOG", "CAT", "Horse"])
# print Animals.DOG
