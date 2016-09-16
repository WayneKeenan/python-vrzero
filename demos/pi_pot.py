#!/usr/bin/python3

import pi3d
from vrzero import engine

# This VR Zero demo is modified version of the original Pi3D demo, found here:
# https://github.com/pi3d/pi3d_demos/blob/master/LoadModelObj.py

engine.init()

shader = pi3d.Shader("uv_reflect")
flat_shader = pi3d.Shader("uv_flat")

ectex = pi3d.loadECfiles("textures/ecubes","sbox")
myecube = pi3d.EnvironmentCube(size=900.0, maptype="FACES", name="bfa", y=50.0)
myecube.set_draw_details(flat_shader, ectex)


# ========================================
# this is a bit of a one off because the texture has transparent parts
# comment out and google to see why it's included here.
pi3d.opengles.glDisable(pi3d.GL_CULL_FACE)

# ========================================
# load bump and reflection textures
bumptex = pi3d.Texture("textures/floor_nm.jpg")
shinetex = pi3d.Texture("textures/stars.jpg")


# ========================================
# load model

mymodel = pi3d.Model(file_string='models/teapot.obj', name='teapot', y=5.0, z=10.0)
mymodel.set_shader(shader)
mymodel.set_normal_shine(bumptex, 16.0, shinetex, 0.5)


def update():
    mymodel.rotateIncY(0.41)
    mymodel.rotateIncZ(0.12)
    mymodel.rotateIncX(0.23)


def draw():
    myecube.draw()
    mymodel.draw()

engine.on_update = update
engine.on_render = draw
engine.start()
