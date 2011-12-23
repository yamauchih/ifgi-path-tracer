#
# ifgi C++ rendering core access API
# Copyright (C) 2011 Yamauchi, Hitoshi
#
import ifgi_cpp_render_mod

ifgicore = ifgi_cpp_render_mod.ifgi_cpp_render()

print dir(ifgicore)

mat_env = {'mat_name': 'default_env',
           'mat_type': 'environment_constant_color',
           'emit_color': '0.1 0.1 0.1 1.0'
           }

ifgicore.add_material(mat_env)
