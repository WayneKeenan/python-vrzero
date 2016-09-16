#!/usr/bin/python3

# This VR Zero demo is modified version of the original Pi3D demo, found here:
# https://github.com/pi3d/pi3d_demos/blob/master/BuckfastAbbey.py

import pi3d
from vrzero import engine
engine.show_stats=True
# VR Zero init, must be done *before* Pi3D setup.
engine.init()

# Pi3D scene setup...
shader = pi3d.Shader("uv_light")
flatsh = pi3d.Shader("uv_flat")

ectex = pi3d.loadECfiles("textures/ecubes","sbox")
myecube = pi3d.EnvironmentCube(size=900.0, maptype="FACES", name="bfa", y=50.0)
myecube.set_draw_details(flatsh, ectex)

mymodel = pi3d.Model( name="Abbey",
                      file_string="models/Buckfast Abbey/BuckfastAbbey.egg",
                      rx=90, sx=0.03, sy=0.03, sz=0.03)
mymodel.set_shader(shader)

# VR Zero config and main loop with Pi3D drawing
engine.avatar_position = [50.0, 0.0, -150.0]

def draw():
    myecube.draw()
    mymodel.draw()

engine.on_render = draw
engine.start()
