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
import ObjReader, IfgiSceneReader, Material
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

        # append material with converting tio a Material (not dict in
        # ifgi_reader)
        assert(len(self.material_list) == len(self.material_name_idx_dict))

        for mat_dict in _ifgi_reader.material_list:
            mat = Material.material_factory(mat_dict)
            self.material_list.append(mat)
            idx = len(self.material_list) - 1
            mat_name = mat_dict['mat_name']
            self.material_name_idx_dict[mat_name] = idx

        assert(len(self.material_list) == len(self.material_name_idx_dict))

        # append geometry (so far added geometry as geo_dict as is)
        assert(len(self.geometry_list) == len(self.geometry_name_idx_dict))

        for geo_dict in _ifgi_reader.geometry_list:
            geo_name = geo_dict['geo_name']
            self.geometry_list.append(geo_dict)
            idx = len(self.geometry_list) - 1
            self.geometry_name_idx_dict[geo_name] = idx

        assert(len(self.geometry_list) == len(self.geometry_name_idx_dict))


    def print_summary(self):
        """print summary"""
        print '# of materials  = ', len(self.material_list)
        print '# of geometries = ', len(self.geometry_list)

        # sanity check
        assert(len(self.material_list) == len(self.material_name_idx_dict))
        assert(len(self.geometry_list) == len(self.geometry_name_idx_dict))

        for mat_name in self.material_name_idx_dict.keys():
            idx = self.material_name_idx_dict[mat_name]
            if(self.material_list[idx].get_material_name() != mat_name):
                raise StandardError, ('invalid material name to index map.')

        print 'material name index map is valid.'


        for geo_name in self.geometry_name_idx_dict.keys():
            idx = self.geometry_name_idx_dict[geo_name]
            if(self.geometry_list[idx]['geo_name'] != geo_name):
                raise StandardError, ('invalid geometry name to index map.')

        print 'geometry name index map is valid.'




# ----------------------------------------

#
# main test
#
# if __name__ == '__main__':
