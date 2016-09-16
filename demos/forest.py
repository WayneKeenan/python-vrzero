#!/usr/bin/python3

# This VR Zero demo is modified version of the original Pi3D demo, found here:
# https://github.com/pi3d/pi3d_demos/blob/master/ForestWalk.py

import math
import pi3d
from vrzero import engine

# VR Zero init, must be done *before* Pi3D setup.
engine.init()

# Pi3D scene setup...

# load shader
shader = pi3d.Shader("uv_bump")
shinesh = pi3d.Shader("uv_reflect")
flatsh = pi3d.Shader("uv_flat")

tree2img = pi3d.Texture("textures/tree2.png")
tree1img = pi3d.Texture("textures/tree1.png")
hb2img = pi3d.Texture("textures/hornbeam2.png")
bumpimg = pi3d.Texture("textures/grasstile_n.jpg")
reflimg = pi3d.Texture("textures/stars.jpg")
rockimg = pi3d.Texture("textures/rock1.jpg")

FOG = ((0.3, 0.3, 0.4, 0.8), 650.0)
TFOG = ((0.2, 0.24, 0.22, 1.0), 150.0)

#myecube = pi3d.EnvironmentCube(900.0,"HALFCROSS")
ectex=pi3d.loadECfiles("textures/ecubes","sbox")
myecube = pi3d.EnvironmentCube(size=900.0, maptype="FACES", name="cube")
myecube.set_draw_details(flatsh, ectex)

# Create elevation map
mapsize = 1000.0
mapheight = 60.0
mountimg1 = pi3d.Texture("textures/mountains3_512.jpg")
mymap = pi3d.ElevationMap("textures/mountainsHgt.png", name="map",
                     width=mapsize, depth=mapsize, height=mapheight,
                     divx=32, divy=32)
mymap.set_draw_details(shader, [mountimg1, bumpimg, reflimg], 128.0, 0.0)
mymap.set_fog(*FOG)

#Create tree models
treeplane = pi3d.Plane(w=4.0, h=5.0)

treemodel1 = pi3d.MergeShape(name="baretree")
treemodel1.add(treeplane.buf[0], 0,0,0)
treemodel1.add(treeplane.buf[0], 0,0,0, 0,90,0)

treemodel2 = pi3d.MergeShape(name="bushytree")
treemodel2.add(treeplane.buf[0], 0,0,0)
treemodel2.add(treeplane.buf[0], 0,0,0, 0,60,0)
treemodel2.add(treeplane.buf[0], 0,0,0, 0,120,0)

#Scatter them on map using Merge shape's cluster function
mytrees1 = pi3d.MergeShape(name="trees1")
mytrees1.cluster(treemodel1.buf[0], mymap, 0.0, 0.0, 400.0, 400.0, 50, "", 8.0, 3.0)
mytrees1.set_draw_details(flatsh, [tree2img], 0.0, 0.0)
mytrees1.set_fog(*TFOG)

mytrees2 = pi3d.MergeShape(name="trees2")
mytrees2.cluster(treemodel2.buf[0], mymap, 0.0, 0.0, 400.0, 400.0, 80, "", 6.0, 3.0)
mytrees2.set_draw_details(flatsh, [tree1img], 0.0, 0.0)
mytrees2.set_fog(*TFOG)

mytrees3 = pi3d.MergeShape(name="trees3")
mytrees3.cluster(treemodel2, mymap,0.0, 0.0, 300.0, 300.0, 20, "", 4.0, 2.0)
mytrees3.set_draw_details(flatsh, [hb2img], 0.0, 0.0)
mytrees3.set_fog(*TFOG)

#Create monument
monument = pi3d.Model(file_string="models/pi3d.obj", name="monument")
monument.set_shader(shinesh)
monument.set_normal_shine(bumpimg, 16.0, reflimg, 0.4)
monument.set_fog(*FOG)
monument.translate(100.0, -mymap.calcHeight(100.0, 235) + 12.0, 235.0)
monument.scale(20.0, 20.0, 20.0)
monument.rotateToY(65)



def update():
    (x, y, z) = engine.avatar_position
    engine.avatar_y_pos = mymap.calcHeight(x, z) + engine.avatar_eye_height

def draw():
    (xm, ym, zm) = engine.avatar_position
    monument.draw()
    mymap.draw()
    if abs(xm) > 300:
      mymap.position(math.copysign(1000,xm), 0.0, 0.0)
      mymap.draw()
    if abs(zm) > 300:
      mymap.position(0.0, 0.0, math.copysign(1000,zm))
      mymap.draw()
      if abs(xm) > 300:
        mymap.position(math.copysign(1000,xm), 0.0, math.copysign(1000,zm))
        mymap.draw()
    mymap.position(0.0, 0.0, 0.0)
    myecube.draw()
    mytrees3.draw()
    mytrees2.draw()
    mytrees1.draw()

engine.on_update = update
engine.on_render = draw
engine.start()
