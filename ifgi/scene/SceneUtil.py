#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#

"""Scene utility
\file
\brief scene related utility.
"""

# import copy, numpy

# import Camera, Primitive, Material, Texture
import ObjReader, IfgiSceneReader
from ifgi.base.ILog import ILog


# SceneGraphTraverseStrategyIF ----------------------------------------

class SceneGeometryMaterialContainer(object):
    """Scene geometry and material container
    """

    def __init__(self):
        """constructor"""
        # global material list
        self.material_list = []
        # global material name -> index of material_def_list
        self.material_name_idx_dict = {}

        # global geometry list
        self.geometry_list = []
        # global geometry name -> index of geometry_def_list
        self.geometry_name_idx_dict = {}


    def append_ifgi_data(self, _ifgi_reader):
        """Append ifgi reader's data to this.

        \param[in] _ifgi_reader ifgi scene reader. This should be
        valid.
        """

        if(not _ifgi_reader.is_valid()):
            raise StandardError, ('ifgi reader is not valid. Have you read a scene?')

        # Note: append appends a list as one element, use extend to
        # concatenate the list
        assert(len(self.material_list) == len(self.material_name_idx_dict))

        offset = len(self.material_list)
        self.material_list.extend(_ifgi_reader.material_list)

        for mat_name in _ifgi_reader.material_name_idx_dict.keys():
            self.material_name_idx_dict[mat_name] =\
                _ifgi_reader.material_name_idx_dict[mat_name] + offset
            assert(self.material_list[self.material_name_idx_dict[mat_name]].get_material_name() == mat_nem)

        # HEREHERE 2011-9-7(Wed)



# ma ----------------------------------------

#
# main test
#
# if __name__ == '__main__':
