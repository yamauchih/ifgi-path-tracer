#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
"""IFGI ExtObjReader
\file
\brief extended obj reader (reader example)"""

import math
import numpy
import string
import exceptions

class ExtObjReader(object):
    """ExtObjReader class. extended obj file reader.

    Current implementation keeps the data once locally. This means
    this needs double size of memory.

    Supported entity
    - inherit from obj file
    - 'v'  x  y  z
      vertex coordinates

    - 'vt' u v [w]
       texture coordinates

    - 'vn' nx ny nz
       normal

    - 'f' vi/ti/ni vi/ti/ni vi/ti/ni
       vertex_idx/texturecoord_index/normal_index
       assume only triangle


    - extension

    - def_material {
        material_name = name_of_material
        material_type = type_of_material
        diffuse_color = 1.0 1.0 1.0
        material_key1 = val1
        material_key2 = val2
      }
      define material parameters

    - material name
      material reference. The following faces are assigned to this material.

    """

    # public: ------------------------------------------------------------

    # default constructor
    def __init__(self):
        """default constructor"""
        self.__curline           = 0

        # public member
        self.material_list     = []
        self.vertex_list       = []
        self.face_idx_list     = []
        self.texcoord_list     = []
        self.texcoord_idx_list = []
        self.normal_list       = []
        self.normal_idx_list   = []


    # read file
    def read(self, _objfname):
        """read file. (public)
        \param[in] _objfname obj file name
        """
        try:
            self.__check_filetype(_objfname)
            with open(_objfname) as infile:
                self.__curline = 1
                while True:
                    read_line_count = self.__parse_line(infile)
                    if(read_line_count == 0):
                        break
                    else:
                        self.__curline = self.__curline + read_line_count

        except StandardError, extrainfo:
            print 'fail to read [' + _objfname + ']', extrainfo


    # get the process list
    def get_process_dict(self, _firstitem_list):
        """get the process list.
        What indices are processed? The processed indices: True.

        Example
           {'face_idx': True, 'texcoord_idx': False, 'normal_idx': True }
        """
        nitem = len(_firstitem_list)
        assert(nitem > 0)

        process_list = [False, False, False]
        i = 0
        while i < nitem:
            if (_firstitem_list[i] != ''):
                process_list[i] = True
            i = i + 1

        process_dict = {'face_idx':     process_list[0],
                        'texcoord_idx': process_list[1],
                        'normal_idx':   process_list[2] }
        return process_dict


    # dump the internal data
    def dump(self):
        """dump the internal data."""
        # self.__curline = 0

        print '--- Vertex coord'
        for i in self.vertex_list:
            print 'v ',
            print i

        print '--- Face'
        for i in self.face_idx_list:
            print 'f ',
            print i

        print '--- Texcoord'
        for i in self.texcoord_list:
            print 'texcoord ',
            print i

        print '--- Normal idx'
        for i in self.normal_idx_list:
            print 'normal ',
            print i

        print '--- texcoord idx'
        for i in self.texcoord_idx_list:
            print 'tex_idx ',
            print i


    # private: ------------------------------------------------------------

    # check the file is obj file or not
    def __check_filetype(self, _objfname):
        """check the file is obj file or not. (private)
        Just check the first line has 'v '"""

        with open(_objfname) as infile:
            line = ''
            while 1:
                line = string.strip(infile.readline())
                if (line[0] != '#'): # skip comment
                    break

            if (len(line) < 2):
                raise StandardError, ('first line is too short, maybe not obj file.')

            sline = line.split()
            if not (sline[0] == 'v' or sline[0] == 'def_material'):
                raise StandardError, ("file line does not start with 'v ' " +
                                      "or 'def_material'")

            # maybe this is obj file


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

        # ^$ line
        if (len(_line) == 0):
            return read_line_count

        # skip comment
        if (_line[0] == '#'):
            return read_line_count

        # split line
        sline = _line.split()
        objcom = sline[0]

        # process one line command (and also detect a multi-line command)
        if (objcom == 'v'):
            if (len(sline) != 4):
                raise StandardError, ('Error: illigal v line at line ' +
                                      str(self.__curline))
            vpos = numpy.array([float(sline[1]), float(sline[2]), float(sline[3])])
            self.vertex_list.append(vpos)
            # print 'DEBUG: vertex:',
            # print vpos

        elif (objcom == 'vn'):
            if (len(sline) != 4):
                raise StandardError, ('Error: illigal vn line at line ' +
                                      str(self.__curline))

            vn = numpy.array([float(sline[1]), float(sline[2]), float(sline[3])])
            self.normal_list.append(vn)

        elif (objcom == 'vt'):
            if (len(sline) == 3):
                tc = numpy.array([float(sline[1]), float(sline[2])])
                self.texcoord_list.append(tc)
            elif (len(sline) == 4):
                tc = numpy.array([float(sline[1]), float(sline[2]), float(sline[3])])
                self.texcoord_list.append(tc)
            else:
                raise StandardError, ('Error: illigal vt line at line ' +
                                      str(self.__curline))

        elif (objcom == 'f'):
            dat       = sline[1:]
            firstitem = dat[0].split('/')
            nitem       = len(firstitem)
            procdict    = self.get_process_dict(firstitem)
            splitteddat = map((lambda x: x.split('/')), dat)

            if (procdict['face_idx'] == True):
                # vertex index exists x[0] means (nth 0 list)
                # (mapcar (function (lambda (x) (nth 0 x))) '((1 2 3) (4 5 6) (7 8 9)))
                # objfile's index start with 1, therefore i minused as x[0]-1.
                self.face_idx_list.append(map((lambda x: int(x[0])-1), splitteddat))

            if (procdict['texcoord_idx'] == True):
                # texture coodinate index exists
                self.texcoord_idx_list.append(map((lambda x: int(x[1])-1), splitteddat))

            if (procdict['normal_idx'] == True):
                # normal index exists
                self.normal_idx_list.append(map((lambda x: int(x[2])-1), splitteddat))

        elif (objcom == 'def_material'):
            # expect '{' in the same line. This line should be 'def_material {'.
            if (sline[1] != '{'):
                raise StandardError, ('Error: def_material line should have "{"')
            if (len(sline) != 2):
                raise StandardError, ('Error: line should be [def_material {], ' +
                                      _line + ', tokens = ' + str(len(sline)))

            read_line_count = self.__parse_material_def_block(_infile)

        else:
            print 'Warning! unsupported entity [' + objcom + '] at line ' +\
                str(self.__curline)

        return read_line_count


    def __parse_material_def_block(self, _infile):
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

        print 'material info: ', mat_dict
        return read_line_count



#
# main test ... test_ExtObjReader
#
if __name__ == '__main__':
    extobjreader = ExtObjReader()
    extobjreader.read('../../sampledata/cornel_box.ifgi')

