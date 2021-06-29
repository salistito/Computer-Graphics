"""
Sebastián Salinas, CC3501, 4/05/20
Tarea1b
"""
# Importación de modulos
import glfw
from OpenGL.GL import *
import sys

import transformations as tr
import basic_shapes as bs
import easy_shaders as es
import scene_graph as sg


INT_BYTES = 4

# Controller
# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.space_position = 0    # Background initial position 
        self.earth_position = 0.5 # Earth initial position
        self.sun_position = 2.5    # Sun initial position

# We will use the global controller as communication with the callback function
controller = Controller() # Here we declare this as a global variable.


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller # Declares that we are going to use the global object controller inside this function.

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon
        print("Toggle GL_FILL/GL_LINE")

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')

# Model
def createTextureBackground():

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    space_texture = es.toGPUShape(bs.createTextureQuad(r"Textures\background-black.png", nx=1, ny=1), GL_REPEAT, GL_LINEAR)
    earth_gpu = es.toGPUShape(bs.createTextureQuad2(r"Textures\earth.png",0,0,1,1), GL_REPEAT, GL_LINEAR)
    sun_gpu = es.toGPUShape(bs.createTextureQuad2(r"Textures\sun.png",0,0,1,1), GL_REPEAT, GL_LINEAR)

    # Creamos uno inicial para cuando se lagea el timer de glfw, para que se vea más bonito
    first_space = sg.SceneGraphNode("first_space")
    first_space.transform = tr.matmul([tr.translate(0, -1, 0), tr.scale(2, 2, 1)])
    first_space.childs += [space_texture]

    # Repeating both top and bot
    up_space = sg.SceneGraphNode("up_space")
    up_space.transform = tr.matmul([tr.translate(0, 2.0, 0), tr.scale(2, 2, 1)]) 
    up_space.childs += [space_texture]
    
    down_space = sg.SceneGraphNode("down_space")
    down_space.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(2, 2, 1)]) 
    down_space.childs += [space_texture]
    
    # earth figure 
    earth = sg.SceneGraphNode("earth")
    earth.transform = tr.matmul([tr.translate(0.7,0.5,0),tr.scale(4,2,1)])
    earth.childs += [earth_gpu]
    
    # sun figure
    sun = sg.SceneGraphNode("sun")
    sun.transform = tr.matmul([tr.translate(-0.7,2.5,0),tr.scale(0.45,0.45,1)])
    sun.childs += [sun_gpu]
    
    # backgorund scene
    gameScene = sg.SceneGraphNode("gameScene")
    gameScene.transform = tr.identity()
    gameScene.childs += [up_space, down_space, first_space,earth,sun]
    
    return gameScene


#View
if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 600

    window = glfw.create_window(width, height, "background", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders 
    pipelineTexture = es.SimpleTextureTransformShaderProgram() # For the background (space) 
    
    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Creating shapes on GPU memory
    textureBackground = createTextureBackground()
    
    controller.space_position = glfw.get_time()
    t0 = glfw.get_time()
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()
        # Update time
        t1 = glfw.get_time()
        td = t0 - t1
        speed = 10 #7
        controller.space_position += (td * speed)
        controller.earth_position +=(td*speed)
        controller.sun_position +=(td*speed)

        # Filling or not the shapes depending on the controller state
        if controller.fillPolygon:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Telling OpenGL to use our shader program
        glUseProgram(pipelineTexture.shaderProgram)

        # Drawing the texture background, Creamos uno inicial para cuando se lagea el timer de glfw, para que se vea más bonito
        if t0 <= 7:
            first_space = sg.findNode(textureBackground, "first_space")
            first_space.transform = tr.matmul([tr.translate(0,-2 + controller.space_position, 0), tr.scale(2, 2, 1)])
            sg.drawSceneGraphNode(textureBackground, pipelineTexture, "transform")
        
        # Modifying only space background
        # This condition translates the space background so it can be seen as a loop
        if controller.space_position < -2:
            controller.space_position = 0
        if controller.earth_position < -4:
            controller.earth_position = 0
        if controller.sun_position < -4:
            controller.sun_position = 0
        
        # Trasladamos los 2 backgrounds para generar sensacion de movimiento,además del sun y la earth 
        up_space = sg.findNode(textureBackground, "up_space")
        up_space.transform = tr.matmul([tr.translate(0, 2.0 + controller.space_position, 0), tr.scale(2, 2, 1)]) 

        down_space = sg.findNode(textureBackground, "down_space")
        down_space.transform = tr.matmul([tr.translate(0,controller.space_position, 0), tr.scale(2, 2, 1)]) 

        earth = sg.findNode(textureBackground,"earth")
        earth.transform = tr.matmul([tr.translate(0.7, 1.1 + controller.earth_position, 0), tr.scale(4, 2, 1)])

        sun = sg.findNode(textureBackground,"sun")
        sun.transform = tr.matmul([tr.translate(-0.7, 1.1 + controller.sun_position, 0), tr.scale(0.45, 0.45, 1)])

        sg.drawSceneGraphNode(textureBackground, pipelineTexture, "transform") #Dibujamos

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
        
        t0 = glfw.get_time() # actualizamos el t0
    glfw.terminate()