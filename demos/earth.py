#!/usr/bin/python3

# This VR Zero demo is modified version of the original Pi3D demo, found here:
# https://github.com/pi3d/pi3d_demos/blob/master/Earth.py

""" Simple textruring of Sphere objects against a plane. The atmosphere has
blend set to True and so has to be drawn after object behind it to allow them
to show through. Normal map used for moon is just a 'normal' pictures so normals
are calculated strangely and create odd shadows.
Uses the import pi3d method to load *everything*
"""

import pi3d
from math import sin, cos
from vrzero import engine

engine.init()

# ========================================
# Setup display and initialise pi3d
shader = pi3d.Shader("uv_light")
shinesh = pi3d.Shader("uv_reflect")
flatsh = pi3d.Shader("uv_flat")
light = pi3d.Light(lightpos=(1.0, 0.0, 0.1))

# ========================================
# Setting 2nd param to True renders 'True' Blending
# (this can be changed later to 'False' with 'cloudimg.blend = False')
cloudimg = pi3d.Texture("textures/earth_clouds.png",True)
earthimg = pi3d.Texture("textures/world_map.jpg")
moonimg = pi3d.Texture("textures/moon.jpg")
starsimg = pi3d.Texture("textures/stars2.jpg")
watimg = pi3d.Texture("textures/water.jpg")
moonbmp = pi3d.Texture("textures/moon_nm.jpg")

# ========================================
# Load shapes

mysphere = pi3d.Sphere(radius=2, slices=24, sides=24, name="earth", z=5.8)
mysphere2 = pi3d.Sphere(radius=2.05, slices=24, sides=24, name="clouds", z=5.8)
mymoon = pi3d.Sphere(radius=0.4, slices=16, sides=16, name="moon")
mymoon2 = pi3d.Sphere(radius=0.15, slices=16, sides=16, name="moon2")
myplane = pi3d.Plane(w=50, h=50, name="stars", z=30)

rot = 0.0
rot1 = 90.0
rot2 = 0.0
m1Rad = 4  # radius of moon orbit
m2Rad = 0.6  # radius moon's moon orbit

engine.avatar_position = [ 0.0, -5.0, -5.0]
engine.avatar_movement_speed = 0.25
engine.avatar_view_speed = 0.25


def update():
    global rot1, rot2
    myplane.rotateIncZ(0.01)
    mysphere.rotateIncY(-0.1)
    mysphere2.rotateIncY(-0.14)
    mymoon.position(mysphere.x() + m1Rad*sin(rot1), mysphere.y(), mysphere.z() - m1Rad*cos(rot1))
    mymoon.rotateIncY(-0.1)
    mymoon2.position(mymoon.x() - m2Rad*sin(rot2), mymoon.y(), mymoon.z() + m2Rad*cos(rot2))
    mymoon2.rotateIncZ(-0.61)
    rot1 += 0.005
    rot2 += 0.021


def draw():
    mysphere.draw(shader, [earthimg])
    mymoon.draw(shinesh, [moonimg, moonbmp], 6.0, 0.0)
    mymoon2.draw(shinesh, [watimg, moonbmp, starsimg], 3.0, 0.8)
    myplane.draw(flatsh,[starsimg])
    mysphere2.draw(shader, [cloudimg])  # this has to be last as blend = True


engine.on_update = update
engine.on_render = draw
engine.start()
