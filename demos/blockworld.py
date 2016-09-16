#!/usr/bin/python3

# Greetings programs...

# Created By User: Wayne Keenan
# ( wayne@thebubbleworks.com  /  https://twitter.com/wkeenan  /  https://github.com/WayneKeenan )

"""
A very basic, not very efficient and not much fun 'Minecraft' wannabe.
"""

import pi3d
from vrzero import engine

# VR Zero init, must be done *before* Pi3D setup.
engine.init()

# Pi3D scene setup...
light_shader = pi3d.Shader("uv_light")
flat_shader = pi3d.Shader("uv_flat")

ectex = pi3d.loadECfiles("textures/ecubes","sbox")
myecube = pi3d.EnvironmentCube(size=900.0, maptype="FACES", name="bfa", y=50.0)
myecube.set_draw_details(flat_shader, ectex)

brick_texture = pi3d.Texture("textures/minecraft/brick1.png")
grass_texture = pi3d.Texture("textures/minecraft/grass1.png")

BLOCK_SIZE = 3

brick_blocks = []       # model data for bricks
grass_blocks = []       # model data for grass

cubes = []       # textured 'Cuboids' (bricks and grass) for rendering

for x in range(-5, 5):
    for z in range(-10, 0):
        grass_blocks.append(( x*BLOCK_SIZE, 0, z*BLOCK_SIZE ))


# Helper function for adding a brick to the model
def brickAt(x, y, z, xo=0, yo=1, zo=-6):
    brick_blocks.append(((x+xo)*BLOCK_SIZE, (y+yo)*BLOCK_SIZE, (z+zo)*BLOCK_SIZE))

# create a 'pi' symbol statue, 5 cubes across the top with each leg being 3 cubes high.
brickAt(-2, 3, 0); brickAt(-1, 3, 0); brickAt(0, 3, 0); brickAt(1, 3, 0); brickAt(2, 3, 0);
brickAt(-1, 2, 0);		brickAt(1, 2, 0)
brickAt(-1, 1, 0);		brickAt(1, 1, 0)
brickAt(-1, 0, 0);		brickAt(1, 0, 0)


for position in brick_blocks:
    brick = pi3d.Cuboid()
    brick.set_draw_details(light_shader, [brick_texture])
    brick.scale(BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    brick.translate(*position)
    cubes.append(brick)

for position in grass_blocks:
    grass = pi3d.Cuboid()
    grass.set_draw_details(light_shader, [grass_texture])
    grass.scale(BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    grass.translate(*position)
    cubes.append(grass)

def on_action_pressed():
    print("FIRE!")


def on_jump_pressed():
    print("JUMP!")



def draw():
    myecube.draw()
    for cube in cubes:
        cube.draw()

engine.avatar_movement_speed = 0.5
engine.avatar_position = [0.0, 0.0, -50.0]

engine.on_action_pressed = on_action_pressed
engine.on_jump_pressed = on_jump_pressed
engine.on_render = draw
engine.start()
