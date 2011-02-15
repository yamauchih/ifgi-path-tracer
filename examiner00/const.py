#!/usr/bin/env python
"""const for python.
\file
\brief const implementation

URL: http://code.activestate.com/recipes/65207/
ut in const.py...:

# that's all -- now any client-code can
import const
# and bind an attribute ONCE:
const.magic = 23
# but NOT re-bind it:
const.magic = 88      # raises const.ConstError
# you may also want to add the obvious __delattr__
"""

# const for python
class _const:
    """const for python."""
    class ConstError(TypeError):
        """const error."""
        pass

    def __setattr__(self,name,value):
        """set attribute."""
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const(%s)"%name
        self.__dict__[name]=value

import sys
sys.modules[__name__]=_const()

