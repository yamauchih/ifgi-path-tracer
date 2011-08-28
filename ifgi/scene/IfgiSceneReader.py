#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
"""IFGI scene reader
\file
\brief ifgi scene reader (reader example)"""

import math, numpy, string, exceptions, os.path

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
        geo_file = filename
        # could be inline, but later
      }

    The geometry should be read after ifgi scene file has been read.
    """

    # public: ------------------------------------------------------------

    def __init__(self):
        """default constructor"""
        self.__curline     = 0

        self.__defined_type_list = ['material', 'geometry']

        self.__ifgi_abspath = ''
        self.__ifgi_dirname = ''

        self.material_list = []
        #    material name -> index of material_def_list
        self.material_name_idx_dict = {}

        # geometry
        self.geometry_list = []
        #    geometry name -> index of geometry_def_list
        self.geometry_name_idx_dict = {}


    def read(self, _ifgi_fname_path):
        """read a ifgi scene file.
        \param[in] _ifgi_fname_path ifgi scene file name
        """
        if (not os.path.isfile(_ifgi_fname_path)):
            raise StandardError, ('no such file [' + _ifgi_fname_path + ']')

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
            print 'fail to read [' + _ifgi_fname_path + ']', extrainfo


    def get_dirname(self):
        """get ifgi scenefile dirname.
        \return ifgi scene file dirname
        """
        return self.__ifgi_dirname


    def dump(self):
        """dump the internal data."""

        print 'file abspath [' + self.__ifgi_abspath + ']'
        print 'dirname [' + self.__ifgi_dirname + ']'

        print '--- material definition'
        for m in self.material_list:
            print 'def_material:', m

        print '--- geometry definition'
        for g in self.geometry_list:
            print 'def_geometry:', g


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
                raise StandardError, ('the first line [' + line +
                                      '] is not an ifgi header.')
            sline = _line.split()
            if ((len(sline) < 3) or (sline[0] != '#') or (sline[1] != 'ifgi_scene')):
                raise StandardError, ('the first line [' + line +
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
        \param[in] _new_mat new material to append.
        """
        # check the material
        if (not self.__is_valid_material(_new_mat)):
            raise StandardError, ('invalid material.')

        if(_new_mat['mat_name'] in self.material_name_idx_dict):
            raise StandardError, ('duplicate material [' + _new_mat['mat_name'] + '].')

        new_mat_idx = len(self.material_list)
        self.material_list.append(_new_mat)
        self.material_name_idx_dict[_new_mat['mat_name']] = new_mat_idx


    def __is_valid_geometry(self, geo):
        """check the geometry information.
        \param[in] geo
        \return True when geometry information is valid.
        """
        necessary_key = ['geo_name', 'material', 'geo_file_name']
        is_success = True
        for k in necessary_key:
            if(not k in geo):
                print 'invalid geometry: missing necessary key [' + k + ']'
                return False

        # material exists?
        if (not (geo['material'] in self.material_name_idx_dict)):
            print 'material is not defined at this point.'
            return False

        # geometry file exists?
        geo_fpath = os.path.join(self.__ifgi_dirname, geo['geo_file_name'])
        if (not os.path.isfile(geo_fpath)):
            print 'file [' + geo_fpath + '] does not exist.'
            return False

        return True


    def __append_geometry(self, _new_geo):
        """append new geometry.
        \param[in] _new_geo new geometry info to append.
        """
        # check the geometry
        if (not self.__is_valid_geometry(_new_geo)):
            raise StandardError, ('invalid geometry.')

        if(_new_geo['geo_name'] in self.geometry_name_idx_dict):
            raise StandardError, ('duplicate geometry [' + _new_geo['geo_name'] + '].')

        new_geo_idx = len(self.geometry_list)
        self.geometry_list.append(_new_geo)
        self.geometry_name_idx_dict[_new_geo['geo_name']] = new_geo_idx

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

        return read_line_count



#
# main test ... test_IfgiSceneReader
#
if __name__ == '__main__':
    ifgireader = IfgiSceneReader()
    ifgireader.read('../../sampledata/cornel_box.ifgi')
    ifgireader.dump()
    
