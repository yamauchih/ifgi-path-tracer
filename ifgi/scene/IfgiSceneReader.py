#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
"""IFGI scene reader
\file
\brief ifgi scene reader (reader example)"""

import math, numpy, string, exceptions, os.path
import ConvReader2Primitive, ObjReader
from ifgi.base.ILog import ILog

class IfgiSceneReader(object):
    """IfgiSceneReader class.

    Scene file structure.

    - header: # ifgi_scene 1
      - '# ... comment'
      - 'ifgi_scene ... ifgi scene file
      - '1          ... version number

    - def material {
        mat_name = name_of_material
        mat_type = type_of_material
        diffuse_color = 1.0 1.0 1.0
        material_key1 = val1
        material_key2 = val2
      }

    - def geometry {
        geo_name = name_of_geometry
        material = material_name
        geo_file_type = obj
        geo_file_name = filename
        # could be inline, but later
      }

    The geometry should be read after ifgi scene file has been read.
    Geometry info also has 'TriMesh' entry. This is contents of geo_file_name.

    - geo_info['geo_name'] = name_of_geometry
    - geo_info['material'] = material_name
    - geo_info['geo_file_type'] = 'obj'
    - geo_info['geo_file_name'] = filename
    - geo_info['TriMesh']  = Primitive.TriMesh object

    - def camera {
        cam_name = name_of_camera
        eye_pos = eye_pos
        view_dir = view_dir
        up_dir = up_dir
        fovy_rad = fovy_rad
        aspect_ratio = aspect_ratio
        z_near = z_near
        z_far = z_far
        projection = projection
        target_dist = target_dist
        focal_length = focal_length
        lens_screen_dist = lens_screen_dist
        lens_film_dis = lens_film_dis
        }

    """

    # supported geometry file format
    __supported_geometry_format = ['obj']


    # public: ------------------------------------------------------------

    def __init__(self):
        """default constructor"""
        self.__curline     = -1

        self.__defined_type_list = ['material', 'geometry', 'camera']

        self.__ifgi_abspath = ''
        self.__ifgi_dirname = ''

        self.material_dict_list = []
        #    material name -> index of material_def_list
        self.material_name_idx_dict = {}

        # geometry
        self.geometry_dict_list = []
        #    geometry name -> index of geometry_def_list
        self.geometry_name_idx_dict = {}

        # camera. This is dict
        self.camera_dict_dict = {}

        # last read status
        self.__is_valid = False


    def read(self, _ifgi_fname_path):
        """read a ifgi scene file.

        ifgi scene file currently not contains geometry data. It
        contain only for the geometry file name. Therefore, the
        geometry file is read after the ifgi scene file has been
        parsed.

        \param[in] _ifgi_fname_path ifgi scene file name
        \return True when read file succeeded
        """
        self.__is_valid = False
        if (self.__curline == 0):
            raise StandardError, ('This reader is not re-entrant. ' +\
                                      'Please create a new one to read another file.')
            return False

        self.__curline = 0
        if (not os.path.isfile(_ifgi_fname_path)):
            raise StandardError, ('no such file [' + _ifgi_fname_path + ']')
            return False

        self.__ifgi_abspath = os.path.abspath(_ifgi_fname_path)
        self.__ifgi_dirname = os.path.dirname(self.__ifgi_abspath)

        try:
            self.__check_filetype(self.__ifgi_abspath)
            with open(self.__ifgi_abspath) as infile:
                self.__curline = 1
                while True:
                    read_line_count = self.__parse_line(infile)
                    if(read_line_count == 0):
                        break
                    else:
                        self.__curline = self.__curline + read_line_count

        except StandardError, extrainfo:
            ILog.error('fail to read [' + _ifgi_fname_path + '] ' + str(extrainfo))
            return False

        # now read geometry files
        self.__read_all_geometry_file()
        self.__is_valid = True
        return True

    def get_dirname(self):
        """get ifgi scenefile dirname.
        \return ifgi scene file dirname
        """
        return self.__ifgi_dirname

    def is_valid(self):
        """is valid scene data?
        When last read succeeded, this is True.

        But the scene file's semantics maight be wrong. Just the
        parser can not find the problem of the scene file.

        \return True when the last read succeeded."""
        return self.__is_valid


    def dump(self):
        """dump the internal data."""

        print 'file abspath [' + self.__ifgi_abspath + ']'
        print 'dirname [' + self.__ifgi_dirname + ']'

        print '--- material definition'
        for m in self.material_dict_list:
            print 'def_material:', m

        print '--- geometry definition'
        for g in self.geometry_dict_list:
            print 'def_geometry:', g

        print '--- camera definition'
        for c in self.camera_dict_dict.keys():
            print 'def_camera:', self.camera_dict_dict[c]


    # private: ------------------------------------------------------------

    # check the file is ifgi scene file or not by magic
    def __check_filetype(self, _ifgi_fname_path):
        """check the file is ifgi file or not.
        magic: # ifgi_scene [version number]
        if not, raise exception
        """
        with open(_ifgi_fname_path) as infile:
            line  = infile.readline()
            if (line == ''):
                raise StandardError, ('unexpected EOF')
            _line = string.strip(line)
            if (len(_line) < len('# ifgi_scene 0')):
                # too short header
                raise StandardError, ('the first line [' + _line +
                                      '] is not an ifgi header.')
            sline = _line.split()
            if ((len(sline) < 3) or (sline[0] != '#') or (sline[1] != 'ifgi_scene')):
                raise StandardError, ('the first line [' + _line +
                                      '] is not an ifgi header.')

            if (int(sline[2]) != 0):
                raise StandardError, ('unknown ifgi scene version [' + line + '].')
        # done


    def __is_valid_material(self, mat):
        """check the material.
        \param[in] mat
        \return True when material is valid.
        """
        necessary_key = ['mat_name', 'mat_type']
        is_success = True
        for k in necessary_key:
            if(not k in mat):
                print 'invalid material: missing necessary key [' + k + ']'
                return False

        return True


    def __append_material(self, _new_mat):
        """append new matrial.
        \param[in] _new_mat new material dict to append.
        """
        # check the material
        if (not self.__is_valid_material(_new_mat)):
            raise StandardError, ('invalid material.')

        if(_new_mat['mat_name'] in self.material_name_idx_dict):
            raise StandardError, ('duplicate material [' + _new_mat['mat_name'] + '].')

        new_mat_idx = len(self.material_dict_list)
        self.material_dict_list.append(_new_mat)
        self.material_name_idx_dict[_new_mat['mat_name']] = new_mat_idx


    def __is_valid_geometry(self, _geo_dict):
        """check the geometry information.
        \param[in] _geo_dict
        \return True when geometry information is valid.
        """
        necessary_key = ['geo_name', 'material', 'geo_file_name']
        is_success = True
        for k in necessary_key:
            if(not k in _geo_dict):
                ILog.error('invalid geometry: missing necessary key [' + k +\
                               '], in the geometry block of line ' + str(self.__curline))
                return False

        # material exists?
        if (not (_geo_dict['material'] in self.material_name_idx_dict)):
            ILog.error('material ['+ _geo_dict['material'] + '] of geometry [' +\
                           _geo_dict['geo_name'] + '] is not defined in the geometry ' +\
                           'block of line ' + str(self.__curline))
            return False

        # geometry file exists?
        geo_fpath = os.path.join(self.__ifgi_dirname, _geo_dict['geo_file_name'])
        if (not os.path.isfile(geo_fpath)):
            ILog.error('file [' + geo_fpath + '] does not exist in the geometry ' +\
                           'block of line ' + str(self.__curline))
            return False

        return True


    def __append_geometry(self, _new_geo_dict):
        """append new geometry.
        \param[in] _new_geo_dict new geometry info dict to append.
        """
        # check the geometry
        if (not self.__is_valid_geometry(_new_geo_dict)):
            raise StandardError, ('invalid geometry.')

        if(_new_geo_dict['geo_name'] in self.geometry_name_idx_dict):
            raise StandardError, ('duplicate geometry [' + _new_geo_dict['geo_name'] + '].')

        new_geo_idx = len(self.geometry_dict_list)
        self.geometry_dict_list.append(_new_geo_dict)
        self.geometry_name_idx_dict[_new_geo_dict['geo_name']] = new_geo_idx

        # I can not set the material global index to the primitive
        # here, because the scene can be constructed by multiple ifgi
        # files.  primitive -> material map should be constructed
        # somewhere else.


    def __is_valid_camera(self, _cam_dict):
        """check the camera dictionary validity.
        """
        necessary_key = ['cam_name', 'eye_pos', 'up_dir']
        is_success = True
        for k in necessary_key:
            if(not k in _cam_dict):
                ILog.error('invalid camera: missing necessary key [' + k +\
                               '], in the camera block of line ' + str(self.__curline))
                return False

        return True


    def __append_camera(self, _new_cam_dict):
        """append new camera dict.
        \param[in] _new_cam new camera info dict to append.
        """
        # check the camera name
        if (not self.__is_valid_camera(_new_cam_dict)):
            raise StandardError, ('invalid camera.')

        cam_name = _new_cam_dict['cam_name']
        if(cam_name in self.camera_dict_dict):
            ILog.warning('duplicate camera name, overridden.')

        self.camera_dict_dict[cam_name] = _new_cam_dict


    def __parse_line(self, _infile):
        """parse a line.
        Depends on the line, this might call parse_{block}.
        \param[in] _infile
        \return number of read lines
        """
        # read one line
        line = _infile.readline()
        read_line_count = 1
        if (line == ''):
            return 0            # read 0 means EOF. no more lines

        _line = string.strip(line)

        # skip ^$ line
        if (len(_line) == 0):
            return read_line_count

        # skip comment
        if (_line[0] == '#'):
            return read_line_count

        # split line
        sline = _line.split()
        token = sline[0]

        # process one token
        if (token == 'def'):
            if (len(sline) != 3):
                raise StandardError, ('Error: def line should be [def defined_id {], ' +
                                      _line)
            if ((not (sline[1] in self.__defined_type_list)) or (sline[2] != '{')):
                raise StandardError, ('Error: def line should have defined types. ' +
                                      str(self.__defined_type_list))

            read_line_count = self.__parse_def_block(_infile, sline[1])
        else:
            print 'Warning! unsupported entity [' + token + '] at line ' +\
                str(self.__curline)

        return read_line_count


    def __parse_def_block(self, _infile, _define_type):
        """parse a material block.
        The first line was 'def_material {'. The block should ended '}'
        The block should be one of the following:
           - key = value line
           - comment line (start with # line)
           - '}'

        \param[in] _infile input file
        \param[in] _define_type ['material', 'geometry']
        \return number of read lines
        """
        def_dict = {}
        read_line_count = 1 # We heve already read 'def _define_type {' line.
        while True:
            line = _infile.readline()
            read_line_count = read_line_count + 1
            if line == '':
                raise StandardError, ('Error: unexpected EOF. def ' + _define_type +
                                      ' starts line ' + str(self.__curline))
            _line = string.strip(line)
            if (_line[0] == '#'):   # skip comment
                # print 'skip comment'
                continue
            elif (_line[0] == '}'): # block end
                # print 'block end at ' + str(self.__curline + read_line_count)
                break
            else:
                # print 'key value line'
                # split lines with ' = ' separator
                sep_start = _line.find(' = ')
                sline     = _line.split(' = ')
                if (sep_start == -1):
                    raise StandardError,\
                        ('Error: def ' + _define_type + ' block: ' +
                         ' The line should be key = value.\n'
                         + 'Note: separator must be [ = ] (include two spaces). line at '
                         + str(self.__curline + read_line_count) + ', line = ' + line)
                # whole string of [start + len(' = ') (== 3):] is the key
                def_dict[sline[0]] = _line[sep_start + 3:]

        # print 'def ', def_dict
        if(_define_type == 'material'):
            self.__append_material(def_dict)
        elif(_define_type == 'geometry'):
            self.__append_geometry(def_dict)
        elif(_define_type == 'camera'):
            self.__append_camera(def_dict)

        return read_line_count

    def __read_all_geometry_file(self):
        """read all geometry files.
        """
        for geoinfo in self.geometry_dict_list:
            self.__read_geometry_file(geoinfo)


    def __read_geometry_file(self, _geoinfo):
        """read single geometry file.
        """
        geo_ftype = _geoinfo['geo_file_type']
        if not (geo_ftype in self.__supported_geometry_format):
            raise StandardError, ('non supported geometry file format ['+ geo_ftype + ']')

        geo_fpath = os.path.join(self.__ifgi_dirname, _geoinfo['geo_file_name'])
        ILog.info('loading [' + geo_fpath + ']')

        if (geo_ftype == 'obj'):
            objreader = ObjReader.ObjReader()
            objreader.read(geo_fpath)
            # objreader.dump()
            tmesh = ConvReader2Primitive.\
                conv_objreader_trimesh(objreader, _geoinfo['geo_name'],
                                       _geoinfo['material'])
            # print tmesh.info_summary()
            _geoinfo['TriMesh'] = tmesh

#
# main test ... test_IfgiSceneReader
#
# see test_IfgiSceneReader.py
#
# if __name__ == '__main__':
#     pass

