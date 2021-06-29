# coding=utf-8
"""
Sebastián Salinas, CC3501-Tarea2c 
Drawing 3D bird herd via scene graph with lighting shader program and texturebackground
"""
import glfw
from OpenGL.GL import *
import numpy as np
import sys

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es
import lighting_shaders as ls
import createBird as cb
import catmullRomSplines as cr
import reader as r
import random

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = False
        self.mousePos = (315.0,280.0) 

# we will use the global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

def cursor_pos_callback(window, x, y): # da la posición del mouse en pantalla con coordenadas
    global controller
    controller.mousePos = (x,y)
    #print("Posicion en x:", controller.mousePos[0])
    #print("Posicion en y:",controller.mousePos[1])

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "3D bird-herd with texturebackground", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Connecting callback functions to handle mouse events:
    # - Cursor moving over the window
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)

    # Assembling the shader program (pipeline)
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Shader program for lighting strategies
    lightingPipeline = ls.SimplePhongShaderProgram()

    # Texture shader program for lighting strategies
    #texturePipeline = ls.SimpleTexturePhongShaderProgram()
    
    # Texture shader program
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()

    # Telling OpenGL to use our shader program, this shader program does not consider lighting
    glUseProgram(mvpPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0) #0.85, 0.85, 0.85, 1.0 -> plomo 0.25 por el 0.85

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(50))
    gpuLaguna = es.toGPUShape(bs.createTextureCube(r"Textures\lagoon.jpg"), GL_REPEAT, GL_LINEAR)
    gpuVines = es.toGPUShape(bs.createTextureQuad(r"Textures\vines.jpg"), GL_REPEAT, GL_LINEAR)
    gpuWater = es.toGPUShape(bs.createDecima6TextureQuad(r"Textures\lagoon.jpg",0.15,0.7,.85,1), GL_REPEAT, GL_LINEAR)
    gpuSky = es.toGPUShape(bs.createDecima6TextureQuad(r"Textures\sky.jpg",0,0,0.475,0.5), GL_REPEAT, GL_LINEAR)
    #gpuSomething = es.toGPUShape(bs.createTextureNormalsCube(r"Path.jpg"), GL_REPEAT, GL_LINEAR)
    #if we want texture with light
    
    # Creating the gpuShapes of the herd
    herdSize = int(sys.argv[2]) if len(sys.argv)>2 else 5
    herd = []
    for i in range(herdSize):
        bird = cb.bird().createBird() #Creamos un pajaro 
        if i%2 == 0:          #los pajaros con indice par van en la fila de abajo
            bird.posX = 3*i   #posiciones difrentes dentro de la bandada dependiendo de su indice
            bird.posY = 0
            bird.posZ =  0
            bird.wingsVelocity = random.randint(5,10)
            bird.location = [-6,-10,-6] #localización en el mundo 3D
            herd.append(bird) #los agregamos a la lista 

        if i%2 != 0:          #los pajaros con indice impar van en la fila de arriba
            bird.posX = 3*i   #posiciones difrentes dentro de la bandada dependiendo de su indice
            bird.posY = 0
            bird.posZ = 3
            bird.wingsVelocity = random.randint(5,10)
            bird.location = [-6,-10,-6] #localización en el mundo 3D
            herd.append(bird) #los agregamos a la lista 
    #---------------------------------------------------------------------------------------------------------
    # Trayectoria de las Aves

    # Number of samples to plot
    N = 250 #1000 inicialente, pero 250 para que sea más rapido el trayecto

    # Transformamos el archivo csv a un array 
    archivo = sys.argv[1]
    array = r.csvToArray(archivo)

    # Obtenemos los N puntos de la interpolación de la o las splines, para que las aves sigan esta trayectoria
    points = cr.merchSplinesPoints(array, N)
    #---------------------------------------------------------------------------------------------------------
    
    # Using the same projection matrix in the whole application
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    cameraSpeed = 0.005  #velocidad del giro de cámara
    posCounter = 0      #Iterador para seguir la ruta de la spline, parte en 0 y aumenta según el paso
    paso = 1       #cuanto se avanza en la spline, si se llega al final será -1 para que se devuelvan los pajaros

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        camX =  10* np.cos(cameraSpeed*controller.mousePos[0]) 
        camY =  0
        camZ =  10* np.cos((cameraSpeed)*controller.mousePos[1]) 
        
        viewPos = np.array([0, 23, 6.25]) 

        view = tr.lookAt(
            viewPos,           
            np.array([camX,camY,camZ]), 
            np.array([0,0,1])
        )
        #glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawShape(gpuAxis, GL_LINES)

        # Drawing the stage
        # Telling OpenGL to use our texture shader program, this shader program does consider lighting
        glUseProgram(textureShaderProgram.shaderProgram) #texturePipeline.shaderProgram si es con texturas
        
        #Para trabajar en 2d estabamos mandando sola una transformación (modelo), ahora son 3
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        
        #Drawing the lagoon
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE,  tr.uniformScale(50)) 
        textureShaderProgram.drawShape(gpuLaguna)

        #Drawing the right Vines
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE,  tr.matmul([tr.translate(-24,0,0),tr.rotationX(90*np.pi / 180), tr.rotationY(90*np.pi / 180), tr.uniformScale(50)])) 
        textureShaderProgram.drawShape(gpuVines)

        #Drawing the left Vines
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE,  tr.matmul([tr.translate(24,0,0), tr.rotationX(90*np.pi / 180), tr.rotationY(90*np.pi / 180), tr.uniformScale(50)])) 
        textureShaderProgram.drawShape(gpuVines)

        #Drawing the Water
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE,  tr.matmul([tr.translate(0,0,-24), tr.uniformScale(50)]))
        textureShaderProgram.drawShape(gpuWater)

        #Drawing the Sky
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE,  tr.matmul([tr.translate(0,0,24), tr.uniformScale(50)])) 
        textureShaderProgram.drawShape(gpuSky)

        # Telling OpenGL to use our shader program, this shader program does consider lighting
        glUseProgram(lightingPipeline.shaderProgram)

        # Setting all uniform shader variables

        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        # TO DO: Explore different parameter combinations to understand their effect!

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), 0, -7.5, 6.25)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001) #no atenua casi nada
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03) #atenua un poco menos
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01) #0-> negro lo que no le llega luz (muy atenuado), 1 -> y tono mas oscuro (pero menos que el 0), el que mas atenua de los 3

        #Para trabajar en 2d estabamos mandando sola una transformación (modelo), ahora son 3
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        

        #Para todas los pajaros en la bandada hacemos la animación de aleteo y movimiento por la spline
        for bird in herd:

            # Angle for the rotation of the wings and the tail
            angle = np.sin(bird.wingsVelocity*glfw.get_time()) 
            if angle <= -0.1: #Para evitar que rote de más y se vea feo (si pasa el -0.1 la ala se desconecta)
                angle = -0.1

            # Moving the wings of the bird and the tail
            rightWingRotationNode = sg.findNode(bird,"rightWing")
            rightWingRotationNode.transform = tr.matmul([tr.translate(-1.0, 0.0, 0.02), tr.rotationY(30* np.pi / 180), tr.rotationY(-angle)]) 
            leftWingRotationNode = sg.findNode(bird,"leftWing")
            leftWingRotationNode.transform = tr.matmul([tr.translate(1.0, 0.0, 0.02), tr.rotationY(-30 * np.pi / 180), tr.rotationY(angle)]) 
            tailRotationNode = sg.findNode(bird,"tail")
            tailRotationNode.transform = tr.matmul([tr.translate(0.0, -0.7, 0.0), tr.rotationX(-angle), tr.scale(0.5, 0.8, 0.2)]) 

            # Moving the birds
            bird.transform = tr.matmul([tr.translate(points[posCounter][0] + bird.posX + bird.location[0], points[posCounter][1] + bird.posY + bird.location[1], points[posCounter][2] + bird.posZ + bird.location[2]),tr.scale(-1,-1,1)])
            
            if paso == -1: #Si se llegó al final y se empieza a retroceder se aplica una reflexión para que el movimiento sea coherente
                bird.transform = tr.matmul([tr.translate(points[posCounter][0] + bird.posX + bird.location[0], points[posCounter][1] + bird.posY + bird.location[1], points[posCounter][2] + bird.posZ + bird.location[2]),tr.scale(1,1,1)])

            # Drawing the Bird
            sg.drawSceneGraphNode(bird, lightingPipeline, "model")
        
        posCounter += paso #Aumentamos el paso para la siguiente iteración

        if posCounter == ((len(array)-3)*N)-1: #Si se llega al final de la spline se cambia el paso
            paso = -1

        if posCounter == 0: #Si se llega al comienzo de la spline se cambia el paso 
            paso = 1

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()