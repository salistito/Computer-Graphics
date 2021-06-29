# coding=utf-8
"""
Sebastián Salinas, CC3501-Tarea3a, 2020-1 
Drawing 3D aquarium, voxels of temperature and fishes with lighting shader program. 
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

import json_reader as r
import voxels as v
import createAquarium as ca
import createFish as cf
import random 

# A class to store camera parameters.
class PolarCamera:

    # Initializing a Camera which moves with polar coordinates 
    def __init__(self):
        self.theta_angle = 0.0
        self.eyeX = 0.0
        self.eyeY = 0.0
        self.eyeZ = 0.0
        self.viewPos = 0.0
        self.view = 0.0
        self.radius = 10
    
    def change_theta_angle(self, dt):
        self.theta_angle += dt

    def change_zoom(self, dr):
        if self.radius > -80 and self.radius < 80: # Impondremos un rango para el radio de la cámara, debido a 
            self.radius += dr                      # que fuera de este rango no se pueden apreciar la escena
        if self.radius<-80:
            self.radius= -79.99
        if self.radius>80:
            self.radius= 79.99


    def update_view(self):
        self.eyeX = self.radius * np.sin(self.theta_angle)
        self.eyeY = self.radius * np.cos(self.theta_angle)

        self.viewPos = np.array([self.eyeX, self.eyeY, self.eyeZ])
        
        self.view = tr.lookAt(
            self.viewPos,
            np.array([0,0,0]),
            np.array([0,0,1])
        )   
        
        return self.view


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = False
        self.polar_camera = PolarCamera()
        self.typeA = False # Voxeles del tipo A
        self.typeB = False # Voxeles del tipo B
        self.typeC = False # Voxeles del tipo C
        self.typeAll = False # Voxeles de todo tipo


    @property
    def camera(self):
        """ Get a camera reference from the controller object. """
        return self.polar_camera

# We will use the global controller as communication with the callback function
controller = Controller()
controller.polar_camera = PolarCamera()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis
    
    elif key == glfw.KEY_A:
        controller.typeA = not controller.typeA

    elif key == glfw.KEY_B:
        controller.typeB = not controller.typeB

    elif key == glfw.KEY_C:
        controller.typeC = not controller.typeC

    elif key == glfw.KEY_D:
        controller.typeAll = not controller.typeAll

    elif key == glfw.KEY_ESCAPE:
        sys.exit()


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Aquarium_view", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shaders programs (pipeline)
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    transparencyPipeline = es.SimpleModelViewProjectionShaderProgram_Transparency()

    # Shader program for lighting strategies
    lightingPipeline = ls.SimplePhongShaderProgram()

    # Telling OpenGL to use our shader program, this shader program does not consider lighting
    glUseProgram(mvpPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
    
    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

    # Enabling face culling
    #glEnable(GL_CULL_FACE) # Lamentablemente recorta zonas de mis peces, asi que no se activará

    # Input
    view_setup_name = sys.argv[1] # View setup file
    view_setup_dict = r.jsonToDict(view_setup_name) # Dictonary for the view setup constants

    # View setup
    filename = view_setup_dict["filename"]  
    t_a = view_setup_dict["t_a"]  
    t_b = view_setup_dict["t_b"]  
    t_c = view_setup_dict["t_c"]  
    n_a = view_setup_dict["n_a"]  
    n_b = view_setup_dict["n_b"] 
    n_c = view_setup_dict["n_c"]
    
    #----------------------------------------------------------------------
    # Load results for temperatures
    path = "Solutions/"
    load_voxels = np.load(path + filename) # Se cargan los datos de la matriz de la solución de la EDP

    W = load_voxels.shape[0] # Ancho de la data
    L = load_voxels.shape[1] # Largo de la data
    H = load_voxels.shape[2] # Alto de la data
    
    # Grilla:
    #limites: (W/h)+1, (L/h)+1 y (H/h)+1
    #-> Ejemplo, h=1 se tiene que (W/h)+1 = 4, (L/h)+1 = 7 y (H/h)+1 = 5
    #h=0.5 -> 7,13,9
    #h=0.2 -> 16,31,21
    #h=0.1 -> 31,61,41
    # Grillado
    #X, Y, Z = np.mgrid[0:W:4j, 0:L:7j, 0:H:5j] 
    
    # Equivalentemente podemos generar la grilla de esta forma:
    Y, X, Z = np.meshgrid(np.linspace(0, L, L),np.linspace(0,W,W),np.linspace(0,H,H))

    """
    # Para debugear y ver que son equivalentes:
    Y_prima,X_prima,Z_prima = np.meshgrid(np.linspace(0, L, 31),np.linspace(0,W,16),np.linspace(0,H,21))
    if X.all()==X_prima.all():
        print("True")
    if Y.all()==Y_prima.all():
        print("True")
    if Z.all()==Z_prima.all():
        print("True")
    """
    #---------------------------------------------------------------------  
    # Generaremos una heurística para calcular un h aproximado.
    # Para poder escalar los peces y que se vean un poco acorde al tamaño del acuario y de los voxeles
    
    if W<10 or L<10 or H<10:
        h = 1.2

    if (W>=10 and W<20) or (L>=10 and L<20) or (H>=10 and H<20):
        h = 0.9 #0.8

    if (W>=20 and W<30) or (L>=20 and L<30) or (H>=20 and H<30):
        h = 0.6 

    if W>=30 or L>=30 or H>=30:
        h = 0.4 

    if (W>=30 and L>=30) or (W>=30 and H>=30) or (L>=30 and H>=30):
        h = 0.3


    # Adaptar el radio y altura de la cámara para que se vea bien para todo tipo de discretización
    controller.polar_camera.radius = 3*(H+(3/h))/2
    controller.polar_camera.eyeZ = 3*(H/2+(3/h))/2 # 3*(H+(3/h))/2
    
    #----------------------------------------------------------------------
    # Colores para los voxeles
    red = [1,0,0]
    green = [0,1,0]
    blue = [0,0,1]

    # Isosuperficies 
    isosurface = v.mergeRandomColorVoxels(X,Y,Z,load_voxels) #Superficie de todos los voxeles
    isosurfaceA = v.mergeVoxels(X,Y,Z,load_voxels,blue,t_a,2) #Superficie de los voxeles adecuados para A
    isosurfaceB = v.mergeVoxels(X,Y,Z,load_voxels,green,t_b,2) #Superficie de los voxeles adecuados para B
    isosurfaceC = v.mergeVoxels(X,Y,Z,load_voxels,red,t_c,2) #Superficie de los voxeles adecuados para C
    
    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(L))
    gpu_surface = es.toGPUShape(isosurface)   #Es una solo gpuShape, me permite dibujarlo extremadamente rapido
    gpu_surfaceA = es.toGPUShape(isosurfaceA) #Es una solo gpuShape, me permite dibujarlo extremadamente rapido
    gpu_surfaceB = es.toGPUShape(isosurfaceB) #Es una solo gpuShape, me permite dibujarlo extremadamente rapido
    gpu_surfaceC = es.toGPUShape(isosurfaceC) #Es una solo gpuShape, me permite dibujarlo extremadamente rapido
    
    # Creating the Aquarium
    aquariumEdges = ca.aquarium().createAquariumEdges(W+(2/h),L+(2/h),H+(3/h)) # Marco del acuario 
    aquariumWindows = ca.aquarium().createAquariumWindows(W+(2/h),L+(2/h),H+(2/h)) # Ventanas del acuario
    #---------------------------------------------------------------------
   
    # Creating all the fishes

    # list for fishesA
    vertices_A = isosurfaceA.vertices # Todos los vertices e indices de la isosuperficie A
    feasiblePoints_A = [] # Lista para guardar todos los posibles puntos donde podrán estar los peces A
    fishes_A = [] # Lista para guardar los peces A
    tailVelocity_A = [] # Lista para guardar las velocidades de las colas 
    orientation_A = [] # Lista para guardar las orientaciones de los peces A
    positions_A = [] # Lista para guardar las posiciones escogidas al azar de las posibles que habían 
    counter_A = 0 # contador para iterar sobre estas listas
    
    # points of isosurfaceA
    for i in range(0,len(vertices_A),6):
        point = (vertices_A[i], vertices_A[i+1], vertices_A[i+2])
        feasiblePoints_A.append(point) # Se guardan todos los posibles puntos para los peces A

    # Creating fishes_A
    for i in range(n_a):
        fish = cf.fish().createClownFish()                      # Se crea el pez
        fishes_A.append(fish)                                   # se añade a la lista
        tailVelocity_A.append(random.randint(5,10))             # número para la velocidad de la cola
        orientation_A.append(30*random.randint(0,12))           # número para la orientación en el mundo 3D
        if len(feasiblePoints_A)>0:                             # Si es posible colocar peces A
            positions_A.append(random.choice(feasiblePoints_A)) # escogo una posición al azar

    #---------------------------------------------------------------------
    
    # list for fishesB
    vertices_B = isosurfaceB.vertices # Todos los vertices e indices de la isosuperficie B
    feasiblePoints_B = [] # Lista para guardar todos los posibles puntos donde podrán estar los peces B
    fishes_B = [] # Lista para guardar los peces B
    tailVelocity_B = [] # Lista para guardar las velocidades de las colas 
    orientation_B = [] # Lista para guardar las orientaciones de los peces B
    positions_B = [] # Lista para guardar las posiciones escogidas al azar de las posibles que habían 
    counter_B = 0 # contador para iterar sobre estas listas
    
    # points of isosurfaceB
    for i in range(0,len(vertices_B),6):
        point = (vertices_B[i], vertices_B[i+1], vertices_B[i+2])
        feasiblePoints_B.append(point) # Se guardan todos los posibles puntos para los peces B

    # Creating fishes_B
    for i in range(n_b):
        fish = cf.fish().createSurgeonFish()                    # Se crea el pez
        fishes_B.append(fish)                                   # se añade a la lista
        tailVelocity_B.append(random.randint(5,10))             # número para la velocidad de la cola
        orientation_B.append(30*random.randint(0,12))           # número para la orientación en el mundo 3D
        if len(feasiblePoints_B)>0:                             # Si es posible colocar peces B
            positions_B.append(random.choice(feasiblePoints_B)) # escogo una posición al azar

    #---------------------------------------------------------------------

    # list for fishesC
    vertices_C = isosurfaceC.vertices # Todos los vertices e indices de la isosuperficie C
    feasiblePoints_C = [] # Lista para guardar todos los posibles puntos donde podrán estar los peces C
    fishes_C = [] # Lista para guardar los peces C
    tailVelocity_C = [] # Lista para guardar las velocidades de las colas 
    orientation_C = [] # Lista para guardar las orientaciones de los peces C
    positions_C = [] # Lista para guardar las posiciones escogidas al azar de las posibles que habían 
    counter_C = 0 # contador para iterar sobre estas listas
    
    # points of isosurfaceC
    for i in range(0,len(vertices_C),6):
        point = (vertices_C[i], vertices_C[i+1], vertices_C[i+2])
        feasiblePoints_C.append(point) # Se guardan todos los posibles puntos para los peces C

    # Creating fishes_C
    for i in range(n_c):
        fish = cf.fish().createShark()                          # Se crea el pez
        fishes_C.append(fish)                                   # se añade a la lista
        tailVelocity_C.append(random.randint(5,10))             # número para la velocidad de la cola
        orientation_C.append(30*random.randint(0,12))           # número para la orientación en el mundo 3D
        if len(feasiblePoints_C)>0:                             # Si es posible colocar peces C
            positions_C.append(random.choice(feasiblePoints_C)) # escogo una posición al azar

    #----------------------------------------------------------------------
    t0 = glfw.get_time()
    camera_theta = np.pi/4
    
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        camera = controller.camera

        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            camera.change_theta_angle(2 * dt)

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            camera.change_theta_angle(-2 * dt)
        
        if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
            camera.change_zoom((-3*(H+(3/h))/2) * dt)

        if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
            camera.change_zoom((3*(H+(3/h))/2) * dt)

        view = controller.camera.update_view()
        
        # Setting up the view transform
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        # Setting up the projection transform
        projection = tr.perspective(60, float(width)/float(height), 0.1, 100)
        glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if (controller.showAxis):
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawShape(gpuAxis, GL_LINES)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Telling OpenGL to use our shader program, this shader program does consider lighting
        glUseProgram(lightingPipeline.shaderProgram)

        # Setting all uniform shader variables

        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        # Object is visible at only ambient. Diffuse behavior is almost white. Sparkles are white
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.75, 0.75, 0.75) #0.2 0.2 0.2
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        # TO DO: Explore different parameter combinations to understand their effect!

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), 0, 0,H+(5/h)) #-4.5, 0, 4.5
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), camera.viewPos[0], camera.viewPos[1], camera.viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001) #no atenua casi nada
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03) #atenua un poco menos
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01) #0-> negro lo que no le llega luz (muy atenuado), 1 -> y tono mas oscuro (pero menos que el 0), el que mas atenua de los 3

        #Para trabajar en 2d estabamos mandando sola una transformación (modelo), ahora son 3
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        
        # Drawing the aquariumEdges
        aquariumEdgesNode = sg.findNode(aquariumEdges,"aquarium")
        aquariumEdgesNode.transform = tr.matmul([tr.translate(0,(L+(2/h))/2,-(1/h)),tr.uniformScale(1)])
        sg.drawSceneGraphNode(aquariumEdges, lightingPipeline, "model")

        # Drawing the fishes 
        if len(feasiblePoints_A) > 0:
            for fish in fishes_A:
                fishBodyNode = sg.findNode(fish,"clownFish")
                fishBodyNode.transform = tr.matmul([
                    tr.translate(-W/2,-L/2,0),
                    tr.translate(positions_A[counter_A][0], positions_A[counter_A][1], positions_A[counter_A][2]),
                    tr.rotationZ(orientation_A[counter_A]* np.pi / 180),
                    tr.scale(0.5/h,0.5/h,0.5/h)
                ]) 
            
                # Angle for moving the tail of the fishes
                angle = np.sin(tailVelocity_A[counter_A]*glfw.get_time())

                fishTailRotationNode = sg.findNode(fish,"tail")
                fishTailRotationNode.transform = tr.matmul([
                    tr.translate(0.0, -1.0, 0.0),
                    tr.rotationY(90* np.pi / 180),
                    tr.rotationX(-angle), tr.scale(1, 1, 0.2)
                ]) 
            
                sg.drawSceneGraphNode(fish, lightingPipeline, "model")
                counter_A+=1 # Avanzamos el contador para el siguiente pez A

        if len(feasiblePoints_B) > 0:
            for fish in fishes_B:
                fishBodyNode = sg.findNode(fish,"surgeonFish")
                fishBodyNode.transform = tr.matmul([
                    tr.translate(-W/2,-L/2,0),
                    tr.translate(positions_B[counter_B][0], positions_B[counter_B][1], positions_B[counter_B][2]),
                    tr.rotationZ(orientation_B[counter_B]* np.pi / 180),
                    tr.scale(0.5/h,0.5/h,0.5/h)
                ])
            
                # Angle for moving the tail of the fishes
                angle = np.sin(tailVelocity_B[counter_B]*glfw.get_time())

                fishTailRotationNode = sg.findNode(fish,"tail")
                fishTailRotationNode.transform = tr.matmul([tr.translate(0.0, -1.0, 0.0),
                tr.rotationY(90* np.pi / 180),
                tr.rotationX(-angle), tr.scale(1, 1, 0.2)
                ]) 
            
                sg.drawSceneGraphNode(fish, lightingPipeline, "model")
                counter_B+=1 # Avanzamos el contador para el siguiente pez B

        if len(feasiblePoints_C) > 0:
            for fish in fishes_C:
                fishBodyNode = sg.findNode(fish,"shark")
                fishBodyNode.transform = tr.matmul([
                    tr.translate(-W/2,-L/2,0),
                    tr.translate(positions_C[counter_C][0], positions_C[counter_C][1],positions_C[counter_C][2]),
                    tr.rotationZ(orientation_C[counter_C]* np.pi / 180),
                    tr.scale(0.5/h,0.5/h,0.5/h)
                ])
            
                # Angle for moving the tail of the fishes
                angle = np.sin(tailVelocity_C[counter_C]*glfw.get_time())

                fishTailRotationNode = sg.findNode(fish,"tail")
                fishTailRotationNode.transform = tr.matmul([
                    tr.translate(0.0, -1.0, 0.0),
                    tr.rotationY(90* np.pi / 180),
                    tr.rotationX(-angle), tr.scale(1, 1, 0.2)
                ]) 
            
                sg.drawSceneGraphNode(fish, lightingPipeline, "model")
                counter_C+=1 # Avanzamos el contador para el siguiente pez C

        # Reseteando contadores a 0 para la siguiente iteración
        if counter_A==n_a:
            counter_A=0

        if counter_B==n_b:
            counter_B=0

        if counter_C==n_c:
            counter_C=0
        
        # Drawing the voxels

        # Telling OpenGL to use our shader program, this shader program consider transparency
        glUseProgram(transparencyPipeline.shaderProgram)

        if controller.typeC:

            # Drawing shapes with different model transformations
            glUniformMatrix4fv(glGetUniformLocation(transparencyPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(-W/2,-L/2,0),tr.uniformScale(1)]))
            transparencyPipeline.drawShape(gpu_surfaceC)        

        if controller.typeB:

            # Drawing shapes with different model transformations
            glUniformMatrix4fv(glGetUniformLocation(transparencyPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(-W/2,-L/2,0),tr.uniformScale(1)]))
            transparencyPipeline.drawShape(gpu_surfaceB)
        
        if controller.typeA:

            # Drawing shapes with different model transformations
            glUniformMatrix4fv(glGetUniformLocation(transparencyPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(-W/2,-L/2,0),tr.uniformScale(1)]))
            transparencyPipeline.drawShape(gpu_surfaceA)
        
        if controller.typeAll:

            # Drawing shapes with different model transformations
            glUniformMatrix4fv(glGetUniformLocation(transparencyPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(-W/2,-L/2,0),tr.uniformScale(1)]))
            transparencyPipeline.drawShape(gpu_surface)

        # Drawing the windows of the aquarium
        # Telling OpenGL to use our shader program, this shader program consider transparency
        glUseProgram(transparencyPipeline.shaderProgram)

        # Drawing the aquariumWindows
        aquariumWindowsNode = sg.findNode(aquariumWindows,"aquarium")
        aquariumWindowsNode.transform = tr.matmul([tr.translate(0,(L+(2/h))/2,-(1/h)),tr.uniformScale(1)])
        sg.drawSceneGraphNode(aquariumWindows, transparencyPipeline, "model")
        
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
