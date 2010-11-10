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


