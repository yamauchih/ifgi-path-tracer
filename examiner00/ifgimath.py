#!/usr/bin/env python
#
# math utility
#

import math
import numpy

# get a rotation matrix (taken from Mesa3.1)
# original function contributed by Erich Boleyn (erich@uruk.org)
#
# \param[in] _angle radian
# \param[in] _rot_axis rotation axis
#
def get_rotation_mat(_angle, _rot_axis):

  x = _rot_axis[0]
  y = _rot_axis[1]
  z = _rot_axis[2]

  mag = math.sqrt( x*x + y*y + z*z );
  if (mag == 0):
      raise StandardError, ('Zero axis')

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




# transform point (x',y',z',1) = A * (x,y,z,1)
def transformPoint(_m44, _v3):
  x  = _m44[0][0]*_v3[0] + _m44[0][1]*_v3[1] + _m44[0][2]*_v3[2] + _m44[0][3];
  y  = _m44[1][0]*_v3[0] + _m44[1][1]*_v3[1] + _m44[1][2]*_v3[2] + _m44[1][3];
  z  = _m44[2][0]*_v3[0] + _m44[2][1]*_v3[1] + _m44[2][2]*_v3[2] + _m44[2][3];
  w1 = _m44[3][0]*_v3[0] + _m44[3][1]*_v3[1] + _m44[3][2]*_v3[2] + _m44[3][3];

  if math.fabs(w1) > 1e-5:
    w = 1.0 / w1;
    return numpy.array([x*w, y*w, z*w])
  else:
    return numpy.array([0, 0, 0])


# transform vector (x',y',z',0) = A * (x,y,z,0)
def transformVector(_m44, _v3):
  x = _m44[0][0]*_v3[0] + _m44[0][1]*_v3[1] + _m44[0][2]*_v3[2];
  y = _m44[1][0]*_v3[0] + _m44[1][1]*_v3[1] + _m44[1][2]*_v3[2];
  z = _m44[2][0]*_v3[0] + _m44[2][1]*_v3[1] + _m44[2][2]*_v3[2];

  return numpy.array([x, y, z])



