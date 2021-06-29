# coding=utf-8
"""
Sebastián Salinas, CC3501-Tarea2c 
Creating 3D bird via scene graph
"""
from OpenGL.GL import *
import numpy as np

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

class bird():
    def __init__(self):
        self.posX = 0 # bird-herd positions at "X" axis
        self.posY = 0 # bird-herd positions at "Y" axis
        self.posZ = 0 # bird-herd positions at "Z" axis
        self.wingsVelocity = 0
        self.location = [0,0,0] # 3D world location

    def createBird(self):
        # Basic GPUshapes
        self.gpuDarkGreenCube = es.toGPUShape(bs.createColorNormalsCube(0,0.5,0))  # anivia 0 1 1
        self.gpuBlackCube = es.toGPUShape(bs.createColorNormalsCube(0,0,0))  # anivia 1 1 1
        self.gpuYellowCube =  es.toGPUShape(bs.createColorNormalsCube(1,1,0))  # anivia 1 1 1
        self.gpuBrownCube = es.toGPUShape(bs.createColorNormalsCube(0.5,0.5,0.5)) # cafe más oscuro -> 102 51 0,  # anivia 0 1 1 # plomo 0.5,0.5,0.5
        self.gpuLightBrownCube =  es.toGPUShape(bs.createColorNormalsCube(0.5,0.5,0.5))  # 0.564,0.25,1 # anivia 1 1 1
    
        # Leaf nodes
        self.darkGreenCubeNode = sg.SceneGraphNode("darkGreenCubeNode")
        self.darkGreenCubeNode.childs = [self.gpuDarkGreenCube]

        self.blackCubeNode = sg.SceneGraphNode("blackCubeNode")
        self.blackCubeNode.childs = [self.gpuBlackCube]

        self.yellowCubeNode = sg.SceneGraphNode("yellowCubeNode")
        self.yellowCubeNode.childs = [self.gpuYellowCube]

        self.brownCubeNode = sg.SceneGraphNode("brownCubeNode")
        self.brownCubeNode.childs = [self.gpuBrownCube]
    
        self.lightBrownCubeNode = sg.SceneGraphNode("lightBrownCubeNode")
        self.brownCubeNode.childs = [self.gpuLightBrownCube]

        # Creating the birdBody
        self.birdBody = sg.SceneGraphNode("birdBody")
        self.birdBody.transform = tr.scale(1.2,1.4,0.8) 
        self.birdBody.childs += [self.gpuBrownCube]
    
        # Creating an wing
        self.wing = sg.SceneGraphNode("wing")
        self.wing.transform = tr.scale(1.2,0.6,0.2) 
        self.wing.childs = [self.gpuLightBrownCube]
    
        # Creating the wings
        self.rightWing = sg.SceneGraphNode("rightWing")
        self.rightWing.transform = tr.translate(-0.9, 0.0, 0.0)
        self.rightWing.childs = [self.wing]

        self.leftWing = sg.SceneGraphNode("leftWing")
        self.leftWing.transform = tr.translate(0.9, 0.0, 0.0)
        self.leftWing.childs = [self.wing]

        # Creating the tail
        self.tail = sg.SceneGraphNode("tail")
        self.tail.transform = tr.matmul([
            tr.translate(0.0, -0.7, 0.0),
            tr.scale(0.5, 0.8, 0.2) 
        ])
        self.tail.childs = [self.gpuDarkGreenCube] #Anivia gpuBlackCube

        # Merching all the things of the body
        self.body = sg.SceneGraphNode("body")
        self.body.transform = tr.identity()
        self.body.childs = [self.birdBody, self.rightWing, self.leftWing, self.tail]

        # Creating the birdHead
        self.birdHead = sg.SceneGraphNode("birdHead")
        self.birdHead.transform = tr.identity()
        self.birdHead.childs += [self.gpuDarkGreenCube]

        # Creating the eyes 
        self.rightEye = sg.SceneGraphNode("rightEye")
        self.rightEye.transform = tr.matmul([
            tr.translate(0.25,0.5,0.15),
            tr.scale(0.2,0.2,0.2)
        ])
        self.rightEye.childs += [self.gpuBlackCube]

        self.leftEye = sg.SceneGraphNode("leftEye")
        self.leftEye.transform = tr.matmul([
            tr.translate(-0.25,0.5,0.15),
            tr.scale(0.2,0.2,0.2)
        ])
        self.leftEye.childs += [self.gpuBlackCube]

        # Creating the beak of the bird
        self.beak = sg.SceneGraphNode("beak")
        self.beak.transform = tr.matmul([
            tr.translate(0.0, 0.7, -0.25),
            tr.scale(0.5, 0.4, 0.2)
        ])
        self.beak.childs = [self.gpuYellowCube]
    
        # Merching all the things of the head
        self.head = sg.SceneGraphNode("head")
        self.head.transform = tr.translate(0, 1.2, 0.5) 
        self.head.childs = [self.birdHead, self.rightEye, self.leftEye, self.beak]

        # bird, the one and only
        self.bird = sg.SceneGraphNode("bird")
        self.bird.transform = tr.matmul([
            tr.translate(0,0,0),
            tr.rotationZ(0* np.pi / 180) #-45 para mirar a cámara, 45 para mirar de lado 
        ])
        self.bird.childs = [self.body, self.head]

        return self.bird