"""
Sebastián Salinas, CC3501, 4/05/20
Tarea1b
"""
#Importamos algunos modulos
from OpenGL.GL import *

import transformations as tr
import basic_shapes as bs
import easy_shaders as es
import scene_graph as sg


INT_BYTES = 4

class bullet():
    def __init__(self):
        self.speed = 0.01 # 0.007

        # Enabling transparencies
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Creating all gpuShapes
        self.gpu_bullet = es.toGPUShape(bs.createTextureQuad(r"Textures\pixel_laser_green.png", nx=1, ny=1), GL_REPEAT,GL_LINEAR)
        self.bullet = sg.SceneGraphNode("bullet")
        self.bullet.transform = tr.matmul([tr.translate(0,0,0),tr.scale(0.1,0.2,1)])
        self.bullet.childs += [self.gpu_bullet]

        # Assembling bullet
        bullet = sg.SceneGraphNode("bullet")
        bullet.transform = tr.matmul([tr.translate(0,0,0),tr.scale(0.1,0.2,1)])
        bullet.childs += [self.gpu_bullet]

    # return bullet
    def get_bullet(self):
        return self.bullet


class enemy_bullet():
    def __init__(self):
        self.speed = 0.01 #0.007

        # Enabling transparencies
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Creating all gpuShapes
        self.gpu_bullet = es.toGPUShape(bs.createTextureQuad(r"Textures\pixel_laser_red.png", nx=1, ny=1), GL_REPEAT,GL_LINEAR)
        self.bullet = sg.SceneGraphNode("bullet")
        self.bullet.transform = tr.matmul([tr.translate(0,0,0),tr.scale(0.1,0.2,1)])
        self.bullet.childs += [self.gpu_bullet]

        # Assembling bullet
        bullet = sg.SceneGraphNode("bullet")
        bullet.transform = tr.matmul([tr.translate(0,0,0),tr.scale(0.1,0.2,1)])
        bullet.childs += [self.gpu_bullet]

    # return bullet
    def get_bullet(self):
        return self.bullet
