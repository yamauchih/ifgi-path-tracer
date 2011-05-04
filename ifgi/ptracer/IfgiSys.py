#!/usr/bin/env python
#
# ifgi path tracer system class
#
"""
\file
\brief ifgi path tracer system class
"""

# ifgi system class
class IfgiSys(object):
    """ifgi system
    - initialize the system
    - configure the system
    - get the component
    - shutdown the system
    """

    # default constructor
    def __init__(self):
        """default constructor"""
        # system status: "up", "down"
        self.__sys_status = "down"


    # start the system
    def start(self):
        """start up the system.
        \return true success.
        """
        if self.__sys_status == "up":
            



