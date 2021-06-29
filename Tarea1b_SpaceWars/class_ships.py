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


#Controller
# A class to store the application control
class Controller:
    def __init__(self):
        self.ship_positionX = 0.0
        self.ship_positionY = 0.0

# We will use the global controller as communication with the callback function
controller = Controller() # Here we declare this as a global variable.

class createShip():
    global controller  # Declares that we are going to use the global object controller inside this function.

    def __init__(self):
        self.hp = 3        # ship's health points
        self.shipX = 0     # X position of ship
        self.shipY = 0     # Y position of ship
        self.bulletX = 0   # X postion of bullet
        self.bulletY = 0   # Y position of bullet

        # Enabling transparencies
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Creating all gpuShapes
        self.gpu_body = es.toGPUShape(bs.createTextureQuad2(r"Textures\blue_ship.png",0,0,1,1), GL_REPEAT, GL_NEAREST)
        self.gpu_superShip = es.toGPUShape(bs.createTextureQuad2(r"Textures\roof.png",0,0,1,1), GL_REPEAT, GL_NEAREST)
        self.gpu_fire = es.toGPUShape(bs.createTextureQuad2(r"Textures\fire.png",0,0,1,1), GL_REPEAT, GL_NEAREST)
       
        # Ship structure
        self.body = sg.SceneGraphNode("body")
        self.body.transform = tr.matmul([tr.translate(0,0,0), tr.scale(0.2,0.4,1)])
        self.body.childs += [self.gpu_body]
 

        self.fire = sg.SceneGraphNode("fire")
        self.fire.transform = tr.matmul([tr.translate(0,0,0),tr.scale(0.2,0.4,1)])
        self.fire.childs += [self.gpu_fire]

        self.superShip = sg.SceneGraphNode("superShip")
        self.superShip.transform = tr.matmul([tr.translate(0,0,0),tr.scale(0.2,0.4,1)])
        self.superShip.childs += [self.gpu_superShip]


        # Assembling the ship
        self.ship = sg.SceneGraphNode("ship")
        self.ship.transform = tr.translate(controller.ship_positionX,controller.ship_positionY,0)
        self.ship.childs += [self.body]
        self.ship.childs += [self.fire]
        self.ship.childs += [self.superShip]
        
        # Assembling the ship
        ship = sg.SceneGraphNode("ship")
        ship.transform = tr.translate(controller.ship_positionX,controller.ship_positionY,0)
        ship.childs += [self.body]
        ship.childs += [self.fire]
        ship.childs += [self.superShip]

    # return ship
    def get_ship(self):
        return self.ship
    # update values
    def update_values(self): # updates positions
        self.ship.transform = tr.translate(controller.ship_positionX,controller.ship_positionY,0)

class createEnemyShip():
    global controller  # Declares that we are going to use the global object controller inside this function.

    def __init__(self):
        self.hp = 1
        self.shipX = 0
        self.shipY = 0
        self.speedX = 0.0007
        self.speedY = 0 
        self.shoot = False
        self.bulletX = 0
        self.bulletY = 0
        self.name = ""

        # Enabling transparencies
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Creating all gpuShapes
        self.gpu_body = es.toGPUShape(bs.createTextureQuad(r"Textures\enemy.png", nx=1, ny=1), GL_REPEAT,GL_LINEAR)
        
        # Ship structure
        self.body = sg.SceneGraphNode("body")
        self.body.transform = tr.matmul([tr.translate(0,0,0), tr.scale(1.4,-1.2,1)])
        self.body.childs += [self.gpu_body]
 
        # Assembling the ship
        self.ship = sg.SceneGraphNode("ship")
        self.ship.transform = tr.translate(self.shipX,self.shipY,0)
        self.ship.childs += [self.body]
        
        # Assembling the ship
        ship = sg.SceneGraphNode("ship")
        ship.transform = tr.translate(self.shipX,self.shipY,0)
        ship.childs += [self.body]

    # return ship
    def get_ship(self):
        return self.ship
    # update values
    def update_values(self): # updates positions
        self.ship.transform = tr.translate(self.shipX ,self.shipY,0)