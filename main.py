from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(0, 1)
scene.set_background_color((0.2, 0.2, 0.2))
scene.set_floor(-0.53, (0.5, 0.25, 0.22))
scene.set_directional_light((1, 0.5, -1), 0.3, (0.85, 0.9, 0.9))

@ti.func
def create_oval(pos, radius, color):
    for i, j, k in ti.ndrange((-64,63),(-64,63),(-64,63)):
        if (i-pos[0])**2 / radius[0]**2 + (j-pos[1])**2 / radius[1]**2  + (k-pos[2])**2 / radius[2]**2 < 1:
            scene.set_voxel(vec3(i, j, k), 2, color)

@ti.func
def create_semicicle(pos,radius,color,zPos): # pos(x,y) radius(r1,r2)
    for i, j in ti.ndrange((-64, 63), (-64, 63)):
        if (i-pos[0])**2 / radius[0]**2 + (j-pos[1])**2 / radius[1]**2 < 1 and j >= pos[1]:
            scene.set_voxel(vec3(i, j,zPos), 2, color)

@ti.func
def create_cicle(pos,radius,color,zPos): # pos(x,y) radius(r1,r2)
    for i, j in ti.ndrange((-64, 63), (-64, 63)):
        if (i-pos[0])**2 / radius[0]**2 + (j-pos[1])**2 / radius[1]**2 < 1:
            scene.set_voxel(vec3(i, j,zPos), 2, color)

@ti.func
def create_column(pos1, pos2, size, interpolate=10):
    for i in range(interpolate):
        create_oval(vec3( pos1[0] + i*(pos2[0]-pos1[0])/interpolate,
                            pos1[1] + i*(pos2[1]-pos1[1])/interpolate,
                            pos1[2] + i*(pos2[2]-pos1[2])/interpolate),
                            (size,size,size),vec3(0.788,0.627,0.666))
    


def head():
    color = vec3(0.788,0.627,0.666) # 201 160 170
    pos = (0,0,0)
    radius = (20,18,20)
    create_oval(pos,radius,color)

def eye():
    black_radius = (5,5)
    left_pos = (-11,2)
    right_pos = (11,2)
    create_cicle(left_pos,black_radius,vec3(0,0,0),19) # 黑
    create_cicle(right_pos,black_radius,vec3(0,0,0),19) # 黑
    white_radius = (2,2)
    left_pos = (-12,4)
    right_pos = (10,4)
    create_cicle(left_pos,white_radius,vec3(1,1,1),19) # 白
    create_cicle(right_pos,white_radius,vec3(1,1,1),19) # 白

def mouse():
    create_semicicle((0,-3),(5,5),vec3(0,0,0),20)
    pos4 = (-4,5,-3,-1) #xleft,xright,ydown,yup 
    for i in range(pos4[0],pos4[1]):
        for j in range(pos4[2],pos4[3]):
            scene.set_voxel(vec3(i, j, 20), 2, vec3(1,1,1))
def tear():
    # tear1 
    pos4 = (-13,-9,-10,0) #xleft,xright,ydown,yup
    for i in range(pos4[0],pos4[1]):
        for j in range(pos4[2],pos4[3]):
            scene.set_voxel(vec3(i, j, 17), 2, vec3(0.647,0.78,0.9))
    # tear2
    pos4 = (9,13,-10,0) #xleft,xright,ydown,yup
    for i in range(pos4[0],pos4[1]):
        for j in range(pos4[2],pos4[3]):
            scene.set_voxel(vec3(i, j, 17), 2, vec3(0.647,0.78,0.9))
def body():
    color = vec3(0.788,0.627,0.666) # 201 160 170
    pos = (0,-20,0)
    radius = (10,8,8)
    create_oval(pos,radius,color)

def limbs():
    pass
    create_column((-13,-23,0),(-8,-15,0),3)
    create_column((13,-23,0),(8,-15,0),3)
    create_column((-6,-20,0),(-6,-32,0),4)
    create_column((6,-20,0),(6,-32,0),4)

@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    head()
    eye()
    mouse()
    tear()
    body()
    limbs()

initialize_voxels()
scene.finish()
