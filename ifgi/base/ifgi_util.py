#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# ifgi base utility
"""
\file
\brief ifgi base utility"""

def has_dict_all_key(_dict, _key_list):
    """check a dict has all key list
    \param[in] _dict     dictionary to be checked
    \param[in] _key_list key list to check
    \return True _dict has all _key_list
    """
    for k in _key_list:
        if not(_dict.has_key(k)):
            return False

    return True

def get_dict_missing_key(_dict, _key_list):
    """get missing key list of _dictd
    \param[in] _dict dictionary to be checked
    \param[in] _key_list key list to check
    \return missing key list. [] when no missing keys
    """
    ret = []
    for k in _key_list:
        if not(_dict.has_key(k)):
            ret.append(k)

    return ret
