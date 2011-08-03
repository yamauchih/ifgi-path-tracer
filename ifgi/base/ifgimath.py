#!/usr/bin/env python
#
# Copyright (C) 2010-2011 Yamauchi, Hitoshi
#
# math utility
"""
\file
\brief ifgi math utility"""


import math
import numpy

#----------------------------------------------------------------------
# normalize vector
def normalize_vec(_v):
  EPSILON = 0.001

  v_len = numpy.linalg.norm(_v)
  assert(v_len > EPSILON)
  return _v / v_len


#----------------------------------------------------------------------
# get a rotation matrix (taken from Mesa3.1)
def getRotationMat(_angle, _rot_axis):
  """get a rotation matrix (taken from Mesa3.1)
  original function contributed by Erich Boleyn (erich@uruk.org)

  \param[in] _angle radian
  \param[in] _rot_axis rotation axis
  """


  x = _rot_axis[0]
  y = _rot_axis[1]
  z = _rot_axis[2]

  mag = math.sqrt( x*x + y*y + z*z );
  if (mag == 0):
      raise StandardError, ('Zero axis: ' + str(_rot_axis))

  s = math.sin(_angle);
  c = math.cos(_angle);

  x /= mag;
  y /= mag;
  z /= mag;

  xx = x * x;
  yy = y * y;
  zz = z * z;
  xy = x * y;
  yz = y * z;
  zx = z * x;
  xs = x * s;
  ys = y * s;
  zs = z * s;
  one_c = 1.0 - c;

  mat = numpy.zeros((4,4))      # mxn is a taple

  mat[0][0] = (one_c * xx) + c;
  mat[0][1] = (one_c * xy) - zs;
  mat[0][2] = (one_c * zx) + ys;
  mat[0][3] = 0.0;

  mat[1][0] = (one_c * xy) + zs;
  mat[1][1] = (one_c * yy) + c;
  mat[1][2] = (one_c * yz) - xs;
  mat[1][3] = 0.0;

  mat[2][0] = (one_c * zx) - ys;
  mat[2][1] = (one_c * yz) + xs;
  mat[2][2] = (one_c * zz) + c;
  mat[2][3] = 0.0;

  mat[3][0] = 0.0;
  mat[3][1] = 0.0;
  mat[3][2] = 0.0;
  mat[3][3] = 1.0;

  return mat

#----------------------------------------------------------------------
# transform point (x',y',z',1) = A * (x,y,z,1)
def transformPoint(_m44, _v3):
  """transform point (x',y',z',1) = A * (x,y,z,1)"""
  x  = _m44[0][0]*_v3[0] + _m44[0][1]*_v3[1] + _m44[0][2]*_v3[2] + _m44[0][3];
  y  = _m44[1][0]*_v3[0] + _m44[1][1]*_v3[1] + _m44[1][2]*_v3[2] + _m44[1][3];
  z  = _m44[2][0]*_v3[0] + _m44[2][1]*_v3[1] + _m44[2][2]*_v3[2] + _m44[2][3];
  w1 = _m44[3][0]*_v3[0] + _m44[3][1]*_v3[1] + _m44[3][2]*_v3[2] + _m44[3][3];

  if math.fabs(w1) > 1e-5:
    w = 1.0 / w1;
    return numpy.array([x*w, y*w, z*w])
  else:
    return numpy.array([0, 0, 0])

#----------------------------------------------------------------------
# transform vector (x',y',z',0) = A * (x,y,z,0)
def transformVector(_m44, _v3):
  """ transform vector (x',y',z',0) = A * (x,y,z,0)"""
  x = _m44[0][0]*_v3[0] + _m44[0][1]*_v3[1] + _m44[0][2]*_v3[2];
  y = _m44[1][0]*_v3[0] + _m44[1][1]*_v3[1] + _m44[1][2]*_v3[2];
  z = _m44[2][0]*_v3[0] + _m44[2][1]*_v3[1] + _m44[2][2]*_v3[2];

  return numpy.array([x, y, z])


#----------------------------------------------------------------------
# 2d point to 3d point map
def mapToSphere(_win_point2d, _win_width, _win_height):
  """2d point to 3d point map

  \param[in]  _point2d point in a window coordinate (numpy array)
  \param[in]  _win_width  window width
  \param[in]  _win_height window height
  \return pos3d, position on a sphere
  """

  assert(_win_width  > 0)
  assert(_win_height > 0)

  wx = _win_point2d[0]
  wy = _win_point2d[1]

  # check _win_point2d is in range
  if ((wx < 0) or (wx >= _win_width) or (wy < 0) or (wy >= _win_height)):
    raise StandardError, ('out of range coordinate [' + str(wx) + ',' + str(wy) +
                          '] should be in [' +
                          str(_win_width) + ',' + str(_win_height) + ']')

  # get window normalized relative to center coordinate
  rel_x = (wx - (_win_width  / 2)) / _win_width
  rel_y = ((_win_height / 2) - wy) / _win_height # inverse screen y

  # get
  sinx       = math.sin(math.pi * rel_x * 0.5);
  siny       = math.sin(math.pi * rel_y * 0.5);
  sinx2siny2 = sinx * sinx + siny * siny;

  z = 0
  if sinx2siny2 < 1:
    z = math.sqrt(1 - sinx2siny2)

  pos3d = numpy.array([sinx, siny, z])
  # print 'DEBUG: mouse ' + str(rel_x) + ' ' + str(rel_y) + ', pos3d ' + str(pos3d)

  return pos3d


# lookat matrix (gluLookAt compatible)
def getLookAtMatrix(_eye, _lookat, _up):
  """lookat matrix (gluLookAt compatible)

  Note: in this camera coordinates, the viewing direction is minus
  direction.

  \param[in]  _eye    eye point
  \param[in]  _lookat lookat point
  \param[in]  _up     up vector
  \return 4x4 gluLookAt matrix
  """

  ez = _eye - _lookat
  ez = ez / numpy.linalg.norm(ez)

  ex = numpy.cross(_up, ez)
  ex = ex / numpy.linalg.norm(ex)

  ey = numpy.cross(ez, ex)
  ey = ey / numpy.linalg.norm(ey)

  rmat = numpy.eye(4)     # 4x4 Identity matrix

  rmat[0][0] = ex[0]
  rmat[0][1] = ex[1]
  rmat[0][2] = ex[2]

  rmat[1][0] = ey[0]
  rmat[1][1] = ey[1]
  rmat[1][2] = ey[2]

  rmat[2][0] = ez[0]
  rmat[2][1] = ez[1]
  rmat[2][2] = ez[2]


  tmat = numpy.eye(4)     # 4x4 Identity matrix
  tmat[0][3] = -_eye[0]
  tmat[1][3] = -_eye[1]
  tmat[2][3] = -_eye[2]

  # not rmat * tmat, * is element-wise multiplication
  lookatmat = numpy.dot(rmat, tmat).transpose()

  return lookatmat
