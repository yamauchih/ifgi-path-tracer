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
        self.curline         = 0
        self.vertex_list     = []
        self.texcoord_list   = []
        self.normal_list     = []
        self.face_idx_list   = []
        self.tex_idx_list    = []
        self.normal_idx_list = []


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
            print 'DEBUG: vertex:',
            print vpos

        # HEREHERE 2010-10-20(Wed)
        # print _line

        elif (objcom == 'vn'):
            print 'NIN: vn'
        elif (objcom == 'vt'):
            print 'NIN: vt'

        elif (objcom == 'f'):
            dat = spline[1:]
            for items in dat:
                item = items.split('/')
                nitem = len(item)
                if (nitem == 1):
                    # vertex only
                    pass
                elif(nitem == 2):
                    # vertex/texcoord
                    pass
                elif(nitem == 3):
                    # vertex/texcoord/normal
                    pass
                else:
                    raise StandardError, ('Error: illigal f line at line ' +
                                          str(self.curline))
        else:
            print 'Warning! unsupported entity [' + objcom + '] at line ' +\
                sssstr(self.curline)



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
# main test
#
if __name__ == '__main__':
    objreader = ObjReader()
    objreader.read('../sampledata/one_tri.obj')
