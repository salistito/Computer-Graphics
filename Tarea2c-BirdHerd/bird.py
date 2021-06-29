# coding=utf-8
"""
Sebastián Salinas, CC3501-Tarea2c 
Drawing 3D bird via scene graph with lighting shader program
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

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.mousePos = (0.0,0.0)


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

    window = glfw.create_window(width, height, "3D bird via scene graph with lighting shader program", None, None)

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

    # Telling OpenGL to use our shader program, this shader program does not consider lighting
    glUseProgram(mvpPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0) #0.85, 0.85, 0.85, 1.0 -> plomo 0.25 por el 0.85

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(7))
    bird = cb.bird().createBird()

    # Using the same view and projection matrices in the whole application
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    # Constants    
    t0 = glfw.get_time()
    camera_theta = np.pi/4
    mouseSpeed = 0.0018 

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera_theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera_theta += 2* dt

        camX = 4.5 * np.sin(camera_theta) 
        camY = 4.5 * np.cos(camera_theta) 

        viewPos = np.array([camX,camY,4.5]) 

        view = tr.lookAt(
            viewPos,           
            np.array([0,0,0]),
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

        # Moving the wings of the bird and the tail
        angle = mouseSpeed*controller.mousePos[1]

        rightWingRotationNode = sg.findNode(bird,"rightWing")
        rightWingRotationNode.transform = tr.matmul([tr.translate(-1.0, 0.0, 0.02), tr.rotationY(30* np.pi / 180), tr.rotationY(-angle)]) 
        leftWingRotationNode = sg.findNode(bird,"leftWing")
        leftWingRotationNode.transform = tr.matmul([tr.translate(1.0, 0.0, 0.02), tr.rotationY(-30 * np.pi / 180), tr.rotationY(angle)]) 
        tailRotationNode = sg.findNode(bird,"tail")
        tailRotationNode.transform = tr.matmul([tr.translate(0.0, -0.7, 0.0), tr.rotationX(-angle), tr.scale(0.5, 0.8, 0.2)]) 
   
        # Telling OpenGL to use our shader program, this shader program does consider lighting
        glUseProgram(lightingPipeline.shaderProgram)

        # Setting all uniform shader variables

        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        # TO DO: Explore different parameter combinations to understand their effect!

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), -4.5, 0, 4.5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001) # no atenua casi nada
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03) # atenua un poco menos
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01) # 0-> negro lo que no le llega luz (muy atenuado), 1 -> y tono mas oscuro (pero menos que el 0), el que mas atenua de los 3

        #Para trabajar en 2d estabamos mandando sola una transformación (modelo), ahora son 3
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE,  tr.identity())

        # Drawing the Bird
        sg.drawSceneGraphNode(bird, lightingPipeline, "model")
        
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()