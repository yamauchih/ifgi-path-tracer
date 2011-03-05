#!/usr/bin/env python
#
# simple enum
#
#
class Enum(set):
    """Enum emulation class"""
    def __getattr__(self, _name):
        if _name in self:
            return _name
        raise AttributeError

# Usage:
# Animals = Enum(["DOG", "CAT", "Horse"])
# print Animals.DOG
