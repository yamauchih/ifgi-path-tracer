#!/usr/bin/env python
#
# ifgi path tracer system class
#
"""
\file
\brief ifgi path tracer system class
"""
from ifgi.base.ILog import ILog

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
        # system status: "up", "stop", "down"
        self.__sys_status = "stop"


    # start the system
    def start(self):
        """start up the system.
        \return true success.
        """
        if self.__sys_status == "up":
            ILog.warn('IfgiSys has already been up.')
        elif self.__sys_status == "stop":
            # some re-init here
            self.__sys_status = "up"
            return True
        elif self.__sys_status == "down":
            ILog.error('Can not restart. It has already been shutdown.')

        return False


    # stop the system. Can start again
    def stop(self):
        """stop the system.
        \return true success.
        """
        if self.__sys_status == "up":
            # some stop process here
            self.__sys_status = "stop"
            return True
        elif self.__sys_status == "stop":
            ILog.warn('IfgiSys has already been stopped.')
        elif self.__sys_status == "down":
            ILog.error('Can not stop. It has already been shutdown.')

        return False

    # shutdown the system. can not start again.
    def shutdown(self):
        """shutdown the system.
        \return true success.
        """
        if self.__sys_status == "up":
            # some shutdown process here
            self.__sys_status = "down"
            return True
        elif self.__sys_status == "stop":
            # some shutdown process here
            self.__sys_status = "down"
            return True
        elif self.__sys_status == "down":
            ILog.error('It has already been shutdown.')

        return False

    # get state
    def state(self):
        """get the current state.
        \return state string {"up", "stop", "down"}
        """
        return self.__sys_status
