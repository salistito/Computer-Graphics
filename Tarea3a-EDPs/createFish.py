# coding=utf-8
"""
Sebastián Salinas, CC3501-Tarea3a 
Creating the class fish and a 3D fish via scene graph
"""
import numpy as np

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

class fish():
    def __init__(self):
        self.posX = 0 # Posición en la manada en el eje X
        self.posY = 0 # Posición en la manada en el eje Y
        self.posZ = 0 # Posición en la manada en el eje Z
        self.localizacion = [0,0,0] # Localización en el mundo 3D

    def createClownFish(self):
        # Basic GPUshapes 
        self.gpuBlackCube = es.toGPUShape(bs.createColorNormalsCube(0,0,0))  
        self.gpuWhiteCube =  es.toGPUShape(bs.createColorNormalsCube(1,1,1))  
        self.gpuOrangeCube = es.toGPUShape(bs.createColorNormalsCube(1,0.549,0)) 
        self.gpuOrangePizza =  es.toGPUShape(bs.createColorNormalsPizza(1,0.549,0))  
    
        # Creating the fishBody
        self.fishBody = sg.SceneGraphNode("fishBody")
        self.fishBody.transform = tr.scale(1.0,1.5,1.0) 
        self.fishBody.childs += [self.gpuOrangeCube]

        # Creating a white spot
        self.spot = sg.SceneGraphNode("spot")
        self.spot.transform = tr.scale(1.01,3/14,1.01) 
        self.spot.childs += [self.gpuWhiteCube]

        # Creating the white spots
        self.spot1 = sg.SceneGraphNode("spot1")
        self.spot1.transform = tr.translate(0.0,-6/14,0.0) 
        self.spot1.childs += [self.spot]

        self.spot2 = sg.SceneGraphNode("spot2")
        self.spot2.transform = tr.translate(0.0,0.0,0.0) 
        self.spot2.childs += [self.spot]

        self.spot3 = sg.SceneGraphNode("spot3")
        self.spot3.transform = tr.translate(0.0,6/14,0.0) 
        self.spot3.childs += [self.spot]
    
        # Creating an fin
        self.fin = sg.SceneGraphNode("fin")
        self.fin.transform = tr.scale(0.75,0.75,0.2)
        self.fin.childs = [self.gpuOrangePizza]
    
        # Creating the fins
        self.rightFin = sg.SceneGraphNode("rightFin")
        self.rightFin.transform = tr.matmul([
            tr.translate(-0.75, 0.0, 0.02), 
            tr.rotationZ(-90* np.pi / 180)
        ])
        self.rightFin.childs = [self.fin]

        self.leftFin = sg.SceneGraphNode("leftFin")
        self.leftFin.transform = tr.matmul([
            tr.translate(0.75, 0.0, 0.02), 
            tr.rotationZ(90* np.pi / 180)
        ])
        self.leftFin.childs = [self.fin]

        # Creating the tail
        self.tail = sg.SceneGraphNode("tail")
        self.tail.transform = tr.matmul([
            tr.translate(0.0, -1.0, 0.0),
            tr.rotationY(90* np.pi / 180),
            tr.scale(0.75,0.75, 0.2) 
        ])
        self.tail.childs = [self.gpuOrangePizza] 

        # Merching all the things of the body
        self.body = sg.SceneGraphNode("body")
        self.body.transform = tr.identity()
        self.body.childs = [self.fishBody, self.spot1, self.spot2, self.spot3, self.rightFin, self.leftFin, self.tail]

        # Creating the fishHead
        self.fishHead = sg.SceneGraphNode("fishHead")
        self.fishHead.transform = tr.identity()
        self.fishHead.childs += [self.gpuOrangePizza]

        # Creating the eyes 
        self.rightEye = sg.SceneGraphNode("rightEye")
        self.rightEye.transform = tr.matmul([
            tr.translate(-0.15,-0.2,0.405),
            tr.rotationZ(0* np.pi / 180),
            tr.scale(0.2,0.2,0.2)
        ])
        self.rightEye.childs += [self.gpuBlackCube]

        self.leftEye = sg.SceneGraphNode("leftEye")
        self.leftEye.transform = tr.matmul([
            tr.translate(-0.15,-0.2,-0.405),
            tr.rotationZ(-0*np.pi / 180),
            tr.scale(0.2,0.2,0.2)
        ])
        self.leftEye.childs += [self.gpuBlackCube]

        # Merching all the things of the head
        self.head = sg.SceneGraphNode("head")
        self.head.transform = tr.matmul([
            tr.rotationY(90* np.pi / 180),
            tr.translate(0, 1.25, 0)
        ])
        self.head.childs = [self.fishHead, self.rightEye, self.leftEye]

        # Clownfish, the one and only
        self.clownFish = sg.SceneGraphNode("clownFish")
        self.clownFish.transform = tr.matmul([
            tr.translate(0,0,0),
            tr.rotationZ(0* np.pi / 180) #-45 para mirar a cámara, 45 para mirar de lado 
        ])
        self.clownFish.childs = [self.body, self.head]

        return self.clownFish

    def createSurgeonFish(self):
        # Basic GPUshapes 
        self.gpuBlackCube = es.toGPUShape(bs.createColorNormalsCube(0,0,0))  
        self.gpuBlueCube = es.toGPUShape(bs.createColorNormalsCube(0,0,1))
        self.gpuBluePizza =  es.toGPUShape(bs.createColorNormalsPizza(0,0,1)) 
        self.gpuYellowPizza =  es.toGPUShape(bs.createColorNormalsPizza(1,1,0))  

        # Creating the fishBody
        self.fishBody = sg.SceneGraphNode("fishBody")
        self.fishBody.transform = tr.scale(1.0,1.5,1.0) 
        self.fishBody.childs += [self.gpuBlueCube]

        # Creating a black spot
        self.spot = sg.SceneGraphNode("spot")
        self.spot.transform = tr.scale(1.01,3/14,1.01) 
        self.spot.childs += [self.gpuBlackCube]

        # Creating the black spots
        self.spot1 = sg.SceneGraphNode("spot1")
        self.spot1.transform = tr.translate(0.0,-6/14,0.0) 
        self.spot1.childs += [self.spot]

        self.spot2 = sg.SceneGraphNode("spot2")
        self.spot2.transform = tr.translate(0.0,0.0,0.0) 
        self.spot2.childs += [self.spot]

        self.spot3 = sg.SceneGraphNode("spot3")
        self.spot3.transform = tr.translate(0.0,6/14,0.0) 
        self.spot3.childs += [self.spot]
    
        # Creating an fin
        self.fin = sg.SceneGraphNode("fin")
        self.fin.transform = tr.scale(0.75,0.75,0.2)
        self.fin.childs = [self.gpuYellowPizza]
    
        # Creating the fins
        self.rightFin = sg.SceneGraphNode("rightFin")
        self.rightFin.transform = tr.matmul([
            tr.translate(-0.75, 0.0, 0.02), 
            tr.rotationZ(-90* np.pi / 180)
        ])
        self.rightFin.childs = [self.fin]

        self.leftFin = sg.SceneGraphNode("leftFin")
        self.leftFin.transform = tr.matmul([
            tr.translate(0.75, 0.0, 0.02), 
            tr.rotationZ(90* np.pi / 180)
        ])
        self.leftFin.childs = [self.fin]

        # Creating the tail
        self.tail = sg.SceneGraphNode("tail")
        self.tail.transform = tr.matmul([
            tr.translate(0.0, -1.0, 0.0),
            tr.rotationY(90* np.pi / 180),
            tr.scale(0.75,0.75, 0.2) 
        ])
        self.tail.childs = [self.gpuYellowPizza] 

        # Merching all the things of the body
        self.body = sg.SceneGraphNode("body")
        self.body.transform = tr.identity()
        self.body.childs = [self.fishBody, self.spot1, self.spot2, self.spot3, self.rightFin, self.leftFin, self.tail]

        # Creating the fishHead
        self.fishHead = sg.SceneGraphNode("fishHead")
        self.fishHead.transform = tr.identity()
        self.fishHead.childs += [self.gpuBluePizza]

        # Creating the eyes 
        self.rightEye = sg.SceneGraphNode("rightEye")
        self.rightEye.transform = tr.matmul([
            tr.translate(-0.15,-0.2,0.405),
            tr.rotationZ(0* np.pi / 180),
            tr.scale(0.2,0.2,0.2)
        ])
        self.rightEye.childs += [self.gpuBlackCube]

        self.leftEye = sg.SceneGraphNode("leftEye")
        self.leftEye.transform = tr.matmul([
            tr.translate(-0.15,-0.2,-0.405),
            tr.rotationZ(-0*np.pi / 180),
            tr.scale(0.2,0.2,0.2)
        ])
        self.leftEye.childs += [self.gpuBlackCube]

        # Merching all the things of the head
        self.head = sg.SceneGraphNode("head")
        self.head.transform = tr.matmul([
            tr.rotationY(90* np.pi / 180),
            tr.translate(0, 1.25, 0)
        ])
        self.head.childs = [self.fishHead, self.rightEye, self.leftEye]

        # Surgeonfish, the one and only
        self.surgeonFish = sg.SceneGraphNode("surgeonFish")
        self.surgeonFish.transform = tr.matmul([
            tr.translate(0,0,0),
            tr.rotationZ(0* np.pi / 180) #-45 para mirar a cámara, 45 para mirar de lado 
        ])
        self.surgeonFish.childs = [self.body, self.head]

        return self.surgeonFish

    def createShark(self):
        # Basic GPUshapes 
        self.gpuBlackCube = es.toGPUShape(bs.createColorNormalsCube(0,0,0))  
        self.gpuWhiteCube =  es.toGPUShape(bs.createColorNormalsCube(1,1,1))  
        self.gpuGreyCube = es.toGPUShape(bs.createColorNormalsCube(0.5,0.5,0.5)) 
        self.gpuGreyPizza =  es.toGPUShape(bs.createColorNormalsPizza(0.5,0.5,0.5))
        self.gpuWhitePizza = es.toGPUShape(bs.createColorNormalsPizza(1,1,1))

        # Creating the sharkBody
        self.sharkBody = sg.SceneGraphNode("sharkBody")
        self.sharkBody.transform = tr.scale(1.0,1.5,1.0) 
        self.sharkBody.childs += [self.gpuGreyCube]

        # Creating a gill
        self.gill = sg.SceneGraphNode("gill")
        self.gill.transform = tr.scale(1.01,0.05,0.99) 
        self.gill.childs += [self.gpuBlackCube]

        # Creating the gills
        self.gill1 = sg.SceneGraphNode("gill1")
        self.gill1.transform = tr.translate(0.0,9/14,0.0) 
        self.gill1.childs += [self.gill]

        self.gill2 = sg.SceneGraphNode("gill2")
        self.gill2.transform = tr.translate(0.0,7/14,0.0) 
        self.gill2.childs += [self.gill]

        self.gill3 = sg.SceneGraphNode("gill3")
        self.gill3.transform = tr.translate(0.0,5/14,0.0) 
        self.gill3.childs += [self.gill]
    
        # Creating an fin
        self.fin = sg.SceneGraphNode("fin")
        self.fin.transform = tr.scale(0.75,0.75,0.2)
        self.fin.childs = [self.gpuGreyPizza]
    
        # Creating the fins
        self.rightFin = sg.SceneGraphNode("rightFin")
        self.rightFin.transform = tr.matmul([
            tr.translate(-0.75, 0.0, 0.02), 
            tr.rotationZ(-90* np.pi / 180)
        ])
        self.rightFin.childs = [self.fin]

        self.leftFin = sg.SceneGraphNode("leftFin")
        self.leftFin.transform = tr.matmul([
            tr.translate(0.75, 0.0, 0.02), 
            tr.rotationZ(90* np.pi / 180)
        ])
        self.leftFin.childs = [self.fin]

        self.upFin = sg.SceneGraphNode("upFin")
        self.upFin.transform = tr.matmul([
            tr.translate(0, 0, 1), 
            tr.rotationX(90* np.pi / 180),
            tr.rotationY(90* np.pi / 180)
        ])
        self.upFin.childs = [self.fin]

        # Creating the tail
        self.tail = sg.SceneGraphNode("tail")
        self.tail.transform = tr.matmul([
            tr.translate(0.0, -1.0, 0.0),
            tr.rotationY(90* np.pi / 180),
            tr.scale(0.75,0.75, 0.2) 
        ])
        self.tail.childs = [self.gpuGreyPizza] 

        # Merching all the things of the body
        self.body = sg.SceneGraphNode("body")
        self.body.transform = tr.identity()
        self.body.childs = [self.sharkBody, self.gill1, self.gill2, self.gill3, self.rightFin, self.leftFin, self.upFin, self.tail]

        # Creating the sharkHead
        self.sharkHead = sg.SceneGraphNode("sharkHead")
        self.sharkHead.transform = tr.identity()
        self.sharkHead.childs += [self.gpuGreyPizza]

        # Creating the eyes 
        self.rightEye = sg.SceneGraphNode("rightEye")
        self.rightEye.transform = tr.matmul([
            tr.translate(-0.25,-0.2,0.25),
            tr.rotationZ(-30* np.pi / 180),
            tr.scale(0.2,0.2,0.2)
        ])
        self.rightEye.childs += [self.gpuBlackCube]

        self.leftEye = sg.SceneGraphNode("leftEye")
        self.leftEye.transform = tr.matmul([
            tr.translate(0.25,-0.2,0.25),
            tr.rotationZ(30*np.pi / 180),
            tr.scale(0.2,0.2,0.2)
        ])
        self.leftEye.childs += [self.gpuBlackCube]

        # Creating a tooth
        self.tooth = sg.SceneGraphNode("tooth")
        self.tooth.transform = tr.matmul([
            tr.translate(0,0,0),
            tr.rotationX(90* np.pi / 180),
            tr.rotationY(90* np.pi / 180),
            tr.scale(0.2,0.2,0.025)
        ])
        self.tooth.childs += [self.gpuWhitePizza]

        # Creating the theet
        self.tooth1 = sg.SceneGraphNode("tooth1")
        self.tooth1.transform = tr.identity()
        self.tooth1.childs += [self.tooth]

        self.tooth2= sg.SceneGraphNode("tooth2")
        self.tooth2.transform = tr.translate(0,0.2,0)
        self.tooth2.childs += [self.tooth]

        self.tooth3 = sg.SceneGraphNode("tooth3")
        self.tooth3.transform = tr.translate(0,0.4,0)
        self.tooth3.childs += [self.tooth]

        self.tooth4 = sg.SceneGraphNode("tooth4")
        self.tooth4.transform = tr.matmul([
            tr.translate(0,0,0.2),
            tr.scale(-1,-1,-1)
        ])
        self.tooth4.childs += [self.tooth]

        self.tooth5 = sg.SceneGraphNode("tooth5")
        self.tooth5.transform = tr.matmul([
            tr.translate(0,0.2,0.2),
            tr.scale(-1,-1,-1)
        ])
        self.tooth5.childs += [self.tooth]

        self.tooth6 = sg.SceneGraphNode("tooth6")
        self.tooth6.transform = tr.matmul([
            tr.translate(0,0.4,0.2),
            tr.scale(-1,-1,-1)
        ])
        self.tooth6.childs += [self.tooth]        

        self.teeth = sg.SceneGraphNode("teeth")
        self.teeth.transform = tr.identity()
        self.teeth.childs += [self.tooth1, self.tooth2, self.tooth3, self.tooth4, self.tooth5, self.tooth6]
        
        # Creating the fangs
        self.rightTeeth = sg.SceneGraphNode("righTeeth")
        self.rightTeeth.transform = tr.matmul([
            tr.translate(-0.225,0.05,-0.4),
            tr.rotationZ(-27.5*np.pi / 180)
        ])
        self.rightTeeth.childs += [self.teeth]

        self.leftTeeth = sg.SceneGraphNode("leftTeeth")
        self.leftTeeth.transform = tr.matmul([
            tr.translate(0.225,0.05,-0.4),
            tr.rotationZ(27.5*np.pi / 180)
        ])
        self.leftTeeth.childs += [self.teeth]

        # Merching all the things of the head
        self.head = sg.SceneGraphNode("head")
        self.head.transform = tr.matmul([
            tr.rotationY(0* np.pi / 180),
            tr.translate(0, 1.25, 0)
        ])
        self.head.childs = [self.sharkHead, self.rightEye, self.leftEye, self.rightTeeth, self.leftTeeth]

        # Shark, the one and only
        self.shark = sg.SceneGraphNode("shark")
        self.shark.transform = tr.matmul([
            tr.translate(0,0,0),
            tr.rotationZ(0* np.pi / 180) #-45 para mirar a cámara, 45 para mirar de lado 
        ])
        self.shark.childs = [self.body, self.head]

        return self.shark
