#!/usr/bin/env python
#
# ObjReader
#

"""IFGI ObjReader"""

import math
import numpy
import string
import exceptions

#
# ObjReader class
#
# Current implementation keeps the data once locally.
# This means this needs double size of memory.
#
#
# Supported entity
#  - 'v'  x  y  z
#        vertex coordinates
#
#  - 'vt' u v [w]
#        texture coordinates
#
#  - 'vn' nx ny nz
#        normal
#
#  - 'f' vi/ti/ni vi/ti/ni vi/ti/ni
#        vertex_idx/texturecoord_index/normal_index
#        assume only triangle
#
class ObjReader(object):
    # default constructor
    def __init__(self):
        self.curline           = 0
        self.vertex_list       = []
        self.face_idx_list     = []
        self.texcoord_list     = []
        self.texcoord_idx_list = []
        self.normal_list       = []
        self.normal_idx_list   = []


    # check the file is obj file of not
    # Just check the first line has 'v '
    def check_filetype(self, _objfname):
        with open(_objfname) as infile:
            line = ''
            while 1:
                line = string.strip(infile.readline())
                if (line[0] != '#'): # skip comment
                    break

            if (len(line) < 2):
                raise StandardError, ('first line is too short, maybe not obj file.')

            if not (line[0] == 'v' and line[1] == ' '):
                raise StandardError, ("line does not start with 'v '")

            # maybe this is obj file

    # get the process list
    #
    # example
    #   {'face_idx': True, 'texcoord_idx': False, 'normal_idx': True }
    #
    def get_process_dict(self, _firstitem_list):
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

    # parse line
    #
    # \param[in] _line
    def parse_line(self, _line):

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
                                      str(self.curline))
            vpos = numpy.array([float(sline[1]), float(sline[2]), float(sline[3])])
            self.vertex_list.append(vpos)
            # print 'DEBUG: vertex:',
            # print vpos
        elif (objcom == 'vn'):
            print 'NIN: vn'
        elif (objcom == 'vt'):
            print 'NIN: vt'
        elif (objcom == 'f'):
            dat       = sline[1:]
            firstitem = dat[0].split('/')
            nitem       = len(firstitem)
            procdict    = self.get_process_dict(firstitem)
            splitteddat = map((lambda x: x.split('/')), dat)

            if (procdict['face_idx'] == True):
                # vertex index exists
                self.face_idx_list.append(map((lambda x: int(x[0])), splitteddat))

            if (procdict['texcoord_idx'] == True):
                # texture coodinate index exists
                self.texcoord_idx_list. append(map((lambda x: int(x[1])), splitteddat))

            if (procdict['normal_idx'] == True):
                # normal index exists
                self.normal_idx_list.   append(map((lambda x: int(x[2])), splitteddat))
        else:
            print 'Warning! unsupported entity [' + objcom + '] at line ' +\
                str(self.curline)


    # dump the internal data
    def dump(self):
        # self.curline         = 0

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
        for i in self.tex_idx_list:
            print 'tex_idx ',
            print i



    # read file
    #
    # \param[in] _objfname obj file name
    def read(self, _objfname):
        try:
            self.check_filetype(_objfname)
            with open(_objfname) as infile:
                for line in infile:
                    self.curline = self.curline + 1
                    self.parse_line(string.strip(line))

        except StandardError, extrainfo:
            print 'fail to read [' + _objfname + ']', extrainfo

#
# main test ... test_ObjReader
#
# if __name__ == '__main__':
#     objreader = ObjReader()
#     objreader.read('../sampledata/one_tri.obj')
#
