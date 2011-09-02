#!/usr/bin/env python
#
# Copyright 2011 (C) Yamauchi, Hitoshi
#
"""IFGI ObjReader
\file
\brief simple obj reader (reader example)"""

import math, numpy, string, exceptions


class ObjReader(object):
    """ObjReader class. a simple reader example.

    Current implementation keeps the data once locally. This means
    this needs double size of memory.


    Supported entity
    - 'v'  x  y  z
      vertex coordinates

    - 'vt' u v [w]
       texture coordinates

    - 'vn' nx ny nz
       normal

    - 'f' vi/ti/ni vi/ti/ni vi/ti/ni
       vertex_idx/texturecoord_index/normal_index
       assume only triangle
       """

    # public: ------------------------------------------------------------

    # default constructor
    def __init__(self):
        """default constructor (public)"""
        self.__curline           = 0

        # public member
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
                for line in infile:
                    self.__curline = self.__curline + 1
                    self.__parse_line(string.strip(line))

        except StandardError, extrainfo:
            print 'fail to read [' + _objfname + ']', extrainfo


    # get the process list
    def get_process_dict(self, _firstitem_list):
        """get the process list. (public)
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
        """dump the internal data. (public)"""
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
            while 1:
                line  = infile.readline()
                if (line == ''):
                    raise StandardError, ('unexpected EOF')
                _line = string.strip(line)
                if ((_line != '') and (_line[0] != '#')):
                    # if !comment and !blank line, break and check the file
                    break

            if (len(_line) < 2):
                raise StandardError, ('first line is too short, maybe not obj file.')

            if not (_line[0] == 'v' and _line[1] == ' '):
                raise StandardError, ("line does not start with 'v '")

            # maybe this is obj file

    # parse line
    def __parse_line(self, _line):
        """parse line.  (private)
        \param[in] _line
        """

        # ^$ line
        if (len(_line) == 0):
            return

        # skip comment
        if (_line[0] == '#'):
            return

        # split line
        sline = _line.split()
        objcom = sline[0]
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
        else:
            print 'Warning! unsupported entity [' + objcom + '] at line ' +\
                str(self.__curline)


#
# main test ... test_ObjReader
#
#
# see test_ObjReader.py
#
# if __name__ == '__main__':
#     pass
