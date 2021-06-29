# coding=utf-8
"""
Sebastián Salinas, CC3501-Tarea3a 
Creating the aquarium via scene graph
"""
import numpy as np

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

class aquarium():
    def __init__(self):
        self.posX = 0 # Posición en la manada en el eje X
        self.posY = 0 # Posición en la manada en el eje Y
        self.posZ = 0 # Posición en la manada en el eje Z
        self.localizacion = [0,0,0] # Localización en el mundo 3D

    def createAquariumEdges(self,x,y,z):
        # Basic GPUshapes 
        self.gpuBlackCube = es.toGPUShape(bs.createColorNormalsCube(0,0,0))  

        # Fierro base
        self.fierro = sg.SceneGraphNode("fierro")
        self.fierro.transform = tr.scale(1,1,1) 
        self.fierro.childs += [self.gpuBlackCube]

        # Creating 3 types of edges
        self.fierroX = sg.SceneGraphNode("fierroX")
        self.fierroX.transform = tr.scale(x,0.05,0.05)
        self.fierroX.childs += [self.fierro]

        self.fierroY = sg.SceneGraphNode("fierroY")
        self.fierroY.transform = tr.scale(0.05,y,0.05)
        self.fierroY.childs += [self.fierro]

        self.fierroZ = sg.SceneGraphNode("fierroZ")
        self.fierroZ.transform = tr.scale(0.05,0.05,z)
        self.fierroZ.childs += [self.fierro]
        
        # Creating the edges of the aquarium
        self.fierroX_1 = sg.SceneGraphNode("fierroX_1")
        self.fierroX_1.transform = tr.translate(0,0,0) 
        self.fierroX_1.childs += [self.fierroX]

        self.fierroX_2 = sg.SceneGraphNode("fierroX_2")
        self.fierroX_2.transform = tr.translate(0,-y,0) 
        self.fierroX_2.childs += [self.fierroX]

        self.fierroX_3 = sg.SceneGraphNode("fierroX_3")
        self.fierroX_3.transform = tr.translate(0,0,z) 
        self.fierroX_3.childs += [self.fierroX]

        self.fierroX_4 = sg.SceneGraphNode("fierroX_4")
        self.fierroX_4.transform = tr.translate(0,-y,z)  
        self.fierroX_4.childs += [self.fierroX]

        self.fierroY_1 = sg.SceneGraphNode("fierroY_1")
        self.fierroY_1.transform = tr.translate(-x/2,-y/2,0) 
        self.fierroY_1.childs += [self.fierroY]

        self.fierroY_2 = sg.SceneGraphNode("fierroY_2")
        self.fierroY_2.transform = tr.translate(x/2,-y/2,0)  
        self.fierroY_2.childs += [self.fierroY]

        self.fierroY_3 = sg.SceneGraphNode("fierroY_3")
        self.fierroY_3.transform = tr.translate(-x/2,-y/2,z)  
        self.fierroY_3.childs += [self.fierroY]

        self.fierroY_4 = sg.SceneGraphNode("fierroY_4")
        self.fierroY_4.transform = tr.translate(x/2,-y/2,z)
        self.fierroY_4.childs += [self.fierroY]

        self.fierroZ_1 = sg.SceneGraphNode("fierroZ_1")
        self.fierroZ_1.transform = tr.translate(-x/2,0,z/2)  
        self.fierroZ_1.childs += [self.fierroZ]

        self.fierroZ_2 = sg.SceneGraphNode("fierroZ_2")
        self.fierroZ_2.transform = tr.translate(x/2,0,z/2)  
        self.fierroZ_2.childs += [self.fierroZ]

        self.fierroZ_3 = sg.SceneGraphNode("fierroZ_3")
        self.fierroZ_3.transform = tr.translate(-x/2,-y,z/2)  
        self.fierroZ_3.childs += [self.fierroZ]

        self.fierroZ_4 = sg.SceneGraphNode("fierroZ_4")
        self.fierroZ_4.transform = tr.translate(x/2,-y,z/2)  
        self.fierroZ_4.childs += [self.fierroZ]

        # Juntar los edges en 3 tipos de marcos
        self.marcoX = sg.SceneGraphNode("marcoX")
        self.marcoX.transform = tr.identity()  
        self.marcoX.childs += [self.fierroX_1, self.fierroX_2, self.fierroX_3, self.fierroX_4]

        self.marcoY = sg.SceneGraphNode("marcoY")
        self.marcoY.transform = tr.identity()  
        self.marcoY.childs += [self.fierroY_1, self.fierroY_2, self.fierroY_3, self.fierroY_4]

        self.marcoZ = sg.SceneGraphNode("marcoZ")
        self.marcoZ.transform = tr.identity()
        self.marcoZ.childs += [self.fierroZ_1, self.fierroZ_2, self.fierroZ_3, self.fierroZ_4]

        # Creating the aquarium
        self.aquarium = sg.SceneGraphNode("aquarium")
        self.aquarium.transform = tr.identity() #tr.matmul([tr.translate(0,y/4,0),tr.scale(0.5,0.5,0.5)])
        self.aquarium.childs += [self.marcoX, self.marcoY, self.marcoZ]

        return self.aquarium


    def createAquariumWindows(self,x,y,z):
        # Basic GPUshapes  
        self.gpuCyanCube = es.toGPUShape(bs.createColorCube(0,206/255,209/255)) # darkturquoise rgb(0,206,209) -> (0,206/255,209/255)

        # ventana base
        self.window = sg.SceneGraphNode("window")
        self.window.transform = tr.scale(1,1,1) 
        self.window.childs += [self.gpuCyanCube]

        # Creating 3 types of windows
        self.windowXY = sg.SceneGraphNode("windowXY")
        self.windowXY.transform = tr.scale(x,y,0.05)
        self.windowXY.childs += [self.window]

        self.windowXZ = sg.SceneGraphNode("windowXZ")
        self.windowXZ.transform = tr.scale(x,0.05,z)
        self.windowXZ.childs += [self.window]

        self.windowYZ = sg.SceneGraphNode("windowYZ")
        self.windowYZ.transform = tr.scale(0.05,y,z)
        self.windowYZ.childs += [self.window]

        # Creating the windows of the aquarium
        self.windowXY_1 = sg.SceneGraphNode("windowXY_1")
        self.windowXY_1.transform = tr.translate(0,-y/2,0) 
        self.windowXY_1.childs += [self.windowXY]

        self.windowXY_2 = sg.SceneGraphNode("windowXY_2")
        self.windowXY_2.transform = tr.translate(0,-y/2,z) 
        self.windowXY_2.childs += [self.windowXY]

        self.windowXZ_1 = sg.SceneGraphNode("windowXZ_1")
        self.windowXZ_1.transform = tr.translate(0,0,z/2) 
        self.windowXZ_1.childs += [self.windowXZ]

        self.windowXZ_2 = sg.SceneGraphNode("windowXZ_2")
        self.windowXZ_2.transform = tr.translate(0,-y,z/2)  
        self.windowXZ_2.childs += [self.windowXZ]

        self.windowYZ_1 = sg.SceneGraphNode("windowYZ_1")
        self.windowYZ_1.transform = tr.translate(-x/2,-y/2,z/2) 
        self.windowYZ_1.childs += [self.windowYZ]

        self.windowYZ_2 = sg.SceneGraphNode("windowYZ_2")
        self.windowYZ_2.transform = tr.translate(x/2,-y/2,z/2)  
        self.windowYZ_2.childs += [self.windowYZ]

        # Creating the aquarium
        self.aquarium = sg.SceneGraphNode("aquarium")
        self.aquarium.transform = tr.identity() #tr.matmul([tr.translate(0,y/4,0),tr.scale(0.5,0.5,0.5)]) 
        self.aquarium.childs += [self.windowXY_1, self.windowXY_2,self.windowXZ_1, self.windowXZ_2, self.windowYZ_1, self.windowYZ_2]

        return self.aquarium

