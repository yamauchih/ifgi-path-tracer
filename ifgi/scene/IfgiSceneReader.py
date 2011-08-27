#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
"""IFGI scene reader
\file
\brief ifgi scene reader (reader example)"""

import math
import numpy
import string
import exceptions

class IfgiSceneReader(object):
    """IfgiSceneReader class.

    Scene file structure.

    - header: # ifgi_scene 1
      - '# ... comment'
      - 'ifgi_scene ... ifgi scene file
      - '1          ... version number

    - def_material {
        mat_name = name_of_material
        mat_type = type_of_material
        diffuse_color = 1.0 1.0 1.0
        material_key1 = val1
        material_key2 = val2
      }

    - def_geometry {
        geo_name = name_of_geometry
        material = material_name
        geo_file_type = obj
        geo_file = filename
        # could be inline, but later
      }
    """

    # public: ------------------------------------------------------------

    def __init__(self):
        """default constructor"""
        self.__curline     = 0

        # material
        self.material_def_list = []
        #    material name -> index of material_def_list
        self.material_name_idx_dict = {}

        # geometry
        self.geometry_def_list = []
        #    geometry name -> index of geometry_def_list
        self.geometry_name_idx_dict = {}


    def read(self, _ifgi_fname):
        """read a ifgi scene file.
        \param[in] _ifgi_fname ifgi scene file name
        """
        try:
            self.__check_filetype(_ifgi_fname)
            with open(_ifgi_fname) as infile:
                self.__curline = 1
                while True:
                    read_line_count = self.__parse_line(infile)
                    if(read_line_count == 0):
                        break
                    else:
                        self.__curline = self.__curline + read_line_count

        except StandardError, extrainfo:
            print 'fail to read [' + _ifgi_fname + ']', extrainfo


    # dump the internal data
    def dump(self):
        """dump the internal data."""

        print '--- material definition'
        for m in self.material_def_list:
            print 'def_material:', m

        print '--- geometry definition'
        for g in self.geometry_def_list:
            print 'def_geometry:', g

    # private: ------------------------------------------------------------

    # check the file is ifgi scene file or not by magic
    def __check_filetype(self, _ifgi_fname):
        """check the file is ifgi file or not.
        magic: # ifgi_scene [version number]
        if not, raise exception
        """
        with open(_ifgi_fname) as infile:
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
                is_success = False

        return is_success


    def __append_material(self, _new_mat):
        """append new matrial.
        \param[in] _new_mat new material to append.
        """
        # check the material
        if (not self.__is_valid_material(_new_mat)):
            raise StandardError, ('invalid material.')

        if(_new_mat['mat_name'] in self.material_name_idx_dict):
            raise StandardError, ('duplicate material [' + _new_mat['mat_name']
                                  + '].')

        new_mat_idx = len(self.material_def_list)
        self.material_def_list.append(_new_mat)
        self.material_name_idx_dict[_new_mat['mat_name']] = new_mat_idx

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
        if (token == 'def_material'):
            # expect '{' in the same line. This line should be 'def_material {'.
            if (sline[1] != '{'):
                raise StandardError, ('Error: def_material line should have "{"')
            if (len(sline) != 2):
                raise StandardError, ('Error: line should be [def_material {], ' +
                                      _line + ', tokens = ' + str(len(sline)))

            read_line_count = self.__parse_def_material_block(_infile)

        elif (token == 'def_geometry'):
            # expect '{' in the same line. This line should be 'def_geometry {'.
            if (sline[1] != '{'):
                raise StandardError, ('Error: def_geometry line should have "{"')
            if (len(sline) != 2):
                raise StandardError, ('Error: line should be [def_geometry {], ' +
                                      _line + ', tokens = ' + str(len(sline)))

            print 'NIN def_geometry'
            # read_line_count = self.__parse_geometry_def_block(_infile)

        else:
            print 'Warning! unsupported entity [' + token + '] at line ' +\
                str(self.__curline)

        return read_line_count


    def __parse_def_material_block(self, _infile):
        """parse a material block.
        The first line was 'def_material {'. The block should ended '}'
        The block should be one of the following:
           - key = value line
           - comment line (start with # line)
           - '}'

        \param[in] _infile
        \return number of read lines
        """
        mat_dict = {}
        read_line_count = 1     # We heve already read 'def_material {' line.
        while True:
            line = _infile.readline()
            read_line_count = read_line_count + 1
            if line == '':
                raise StandardError, ('Error: unexpected EOF. material_def starts line '
                                      + str(self.__curline))
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
                        ('Error: def_material block. The line should be key = value.\n'
                         + 'Note: separator must be [ = ] (include two spaces). line at '
                         + str(self.__curline + read_line_count) + ', line = ' + line)
                # whole string of [start + len(' = ') (== 3):] is the key
                mat_dict[sline[0]] = _line[sep_start + 3:]

        # print 'material info: ', mat_dict
        self.__append_material(mat_dict)

        return read_line_count



#
# main test ... test_IfgiSceneReader
#
if __name__ == '__main__':
    ifgireader = IfgiSceneReader()
    ifgireader.read('../../sampledata/cornel_box.ifgi')

