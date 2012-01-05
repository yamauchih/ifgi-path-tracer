#
# ifgi C++ rendering core access API
# Copyright (C) 2011 Yamauchi, Hitoshi
#
import ifgi_cpp_render_mod

ifgicore = ifgi_cpp_render_mod.ifgi_cpp_render()

# print dir(ifgicore)

mat_env = {'mat_name': 'default_env',
           'mat_type': 'environment_constant_color',
           'emit_color': '0.1 0.1 0.1 1.0'
           }
mat_diff = {'mat_name': 'floor_mat',
           'mat_type': 'lambert',
           'diffuse_color': '0.2 0.3 0.4 1.0'
           }

mat_dict_list = [mat_diff, mat_env]
geo_dict_list = []

print 'append a scene'
ifgicore.append_scene(mat_dict_list, geo_dict_list)

print 'set a camera.'
cam = {}
ifgicore.set_camera(cam)

