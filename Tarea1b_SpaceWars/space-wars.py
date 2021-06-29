"""
Sebastián Salinas, CC3501, 7/05/20
Tarea1b
"""
#Importamos algunos modulos
import glfw
from OpenGL.GL import *
import sys

import transformations as tr
import basic_shapes as bs
import easy_shaders as es
import scene_graph as sg
import background as b
import class_ships as cs
import class_bullet as cb
import hitmarker as hit

INT_BYTES = 4

# Controller
# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.shipX = 0.0    # initial position of ship on "X" axis
        self.shipY = -0.7   # initial position of ship on "Y" axis
        self.shoot = False  # boolean value for shooting
        self.bulletX = 0.0  # initial position of bullet on "X" axis
        self.bulletY = -0.4 # initial position of bullet on "Y" axis
        self.earth_position = 0.5 # Earth initial position
        self.sun_position = 2.5 # Sun initial position
        
# We will use the global controller as communication with the callback function
controller = Controller() # Here we declare this as a global variable.

def on_key(window, key, scancode, action, mods):
    global controller  # Declares that we are going to use the global object controller inside this function.
    
    # Keep pressed buttons
    if action == glfw.REPEAT or action == glfw.PRESS: # Presiona cualquier tecla muchas veces o una vez y hace algo 
        if key == glfw.KEY_A:      #Movimiento para la izquierda
            if controller.shipX > -0.90: 
                 controller.shipX -= 0.035
        if key == glfw.KEY_D:      #Movimiento para la derecha
            if controller.shipX < 0.90: 
                controller.shipX += 0.035
        if key == glfw.KEY_W:      #Movimiento para arriba
            if controller.shipY < 0.80: 
                controller.shipY += 0.035
        if key == glfw.KEY_S:      #Movimiento para abajo
            if controller.shipY > -0.80: 
                controller.shipY -= 0.035 
        if key == glfw.KEY_SPACE:  #Disparo con el espacio 
            controller.shoot = True
            
    if action != glfw.PRESS:
        return

    elif key == glfw.KEY_F:  #Rellenar nuestras figuras o no 
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

#View
if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 600

    window = glfw.create_window(width, height, "Space Wars!", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
     # Assembling the shader program (pipeline) with both shaders
    pipelineTexture = es.SimpleTextureTransformShaderProgram() #usuaremos un pipeline de texturas
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipelineTexture.shaderProgram) #Indicamos que usaremos el pipelineTexture.shaderProgram

    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Background
    textureBackground = b.createTextureBackground()

    # Player's Ship
    ship = cs.createShip() 
    shipNode = ship.get_ship() 
    # Bullet
    bullet = cb.bullet()
    bulletNode = bullet.get_bullet

    # enemies
    n = int(sys.argv[1])
    enemies = n
    current = 3    # dibujaremos solo 3 en la escena al principio 
    remaining_enemies = n-3 # estos serán los enemigos restantes 
    enemiesList = [] # lista que contendrá los enemigos
    if n <= 0:
        print("enter a strictly positive number of enemies")

    if n < 3: # caso de poco enemies 
        for i in range(1, n + 1):
            enemy = cs.createEnemyShip() # creamos los enemies 
            enemyNode = enemy.get_ship()   # obtenemos el nodo
            enemy.shipX = -0.6 + (i-1)*0.6  # posiciones difrentes dependiendo de su indice
            enemy.shipY = 1.5 
            name = str(i)
            enemy.name = name
            enemiesList.append(enemy) # los agregamos a una lista 

            enemyBullet = cb.enemy_bullet()
            enemyBulletNode = enemyBullet.get_bullet

    if n >=3: # caso de muchos enemies 
        for i in range(1, 4):
            enemy = cs.createEnemyShip() # creamos los enemies 
            enemyNode = enemy.get_ship()   # obtenemos el nodo
            enemy.shipX = -0.6 + (i-1)*0.6  # posiciones difrentes dependiendo de su indice
            enemy.shipY = 1.5 
            name = str(i)
            enemy.name = name
            enemiesList.append(enemy) # los agregamos a una lista 

            enemyBullet = cb.enemy_bullet()
            enemyBulletNode = enemyBullet.get_bullet

    # GameOver animation
    gpuGame_over = es.toGPUShape(bs.createTextureQuad2(r"Textures\game_over.png",0.325,0.20,0.423,0.332), GL_REPEAT, GL_NEAREST)
    # You Win animation
    gpuYou_win = es.toGPUShape(bs.createTextureQuad2(r"Textures\green_win.png",0,0,1,1), GL_REPEAT, GL_NEAREST)

    t0 = glfw.get_time()
    textureBackground.space_position = glfw.get_time()
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()
        # Update time
        t1 = glfw.get_time()
        td = t0 - t1
        speed = 10 
        textureBackground.space_position += (td * speed)
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

        # Drawing the texture background, creamos uno inicial para cuando se lagea el timer de glfw, para que se vea más bonito
        if t0 <= 15:
            first_space = sg.findNode(textureBackground, "first_space")
            first_space.transform = tr.matmul([tr.translate(0,-2 + textureBackground.space_position, 0), tr.scale(2, 2, 1)])
            sg.drawSceneGraphNode(textureBackground, pipelineTexture, "transform")
        
        # Modifying only space background
        # This condition translates the space background so it can be seen as a loop
        if textureBackground.space_position < -2:
            textureBackground.space_position = 0
        if controller.earth_position < -4:
            controller.earth_position = 0
        if controller.sun_position < -4:
            controller.sun_position = 0
        
        #Trasladamos los 2 fondos para generar sensacion de movimiento
        up_space = sg.findNode(textureBackground, "up_space")
        up_space.transform = tr.matmul([tr.translate(0, 2.0 + textureBackground.space_position, 0), tr.scale(2, 2, 1)]) 

        down_space = sg.findNode(textureBackground, "down_space")
        down_space.transform = tr.matmul([tr.translate(0,textureBackground.space_position, 0), tr.scale(2, 2, 1)]) 

        #trasladamos la figura de la earth
        earth = sg.findNode(textureBackground,"earth")
        earth.transform = tr.matmul([tr.translate(0.7, 1.1 + controller.earth_position, 0), tr.scale(4, 2, 1)])

        #trasladamos la figura del sun 
        sun = sg.findNode(textureBackground,"sun")
        sun.transform = tr.matmul([tr.translate(-0.7, 1.1 + controller.sun_position, 0), tr.scale(0.45, 0.45, 1)])

        sg.drawSceneGraphNode(textureBackground, pipelineTexture, "transform") #Dibujamos
        
        #Iniciamos el juego, si nuesta vida es mayor que 0 
        if ship.hp > 0:
            # Drawing the ship
            # Creating shapes on GPU memory
            ship.update_values() # updateamos los valores de posición 
            shipNode = ship.get_ship() 
            shipNode.transform = tr.translate(controller.shipX,controller.shipY,0) # trasladamos a la posición actual 
            fireNode = sg.findNode(shipNode, "fire")
            supershipNode = sg.findNode(shipNode,"superShip")
            sg.drawSceneGraphNode(shipNode, pipelineTexture, "transform") # dibujamos

            # Ship animation, irá alternando con el tiempo 
            if int(glfw.get_time()%3) == 0:
                supershipNode.transform = tr.scale(0,0,0)
                fireNode.transform = tr.scale(0,0,0)
            if int(glfw.get_time()%3) == 1:
                fireNode.transform = tr.matmul([tr.translate(0,-0.18,0),tr.scale(0.22,0.22,1)])
                supershipNode.transform = tr.scale(0,0,0)  
            if int(glfw.get_time()%3) == 2:
                supershipNode.transform = tr.matmul([tr.translate(0.042,0.0375,0),tr.scale(0.425,0.425,1)])

            # Drawing the enemies
            # Creating shapes on GPU memory 
            for enemy in enemiesList:
                if enemy.hp > 0 or enemy.shoot ==True: # Para que se mantenga dibujado el disparo si es que justo muere
                    enemy.update_values() # updateamos los valores
                    enemyNode = enemy.get_ship() # obtenemos el nodo
                    enemyNode.transform = tr.matmul([tr.translate(enemy.shipX,enemy.shipY, 0),tr.scale(0.2,0.45,1)]) #tr.scale(1.4,-1.2,0)
                    sg.drawSceneGraphNode(enemyNode, pipelineTexture, "transform") #dibujamos

                    # enemies movement 
                    enemy.shipX += enemy.speedX #se mueven en x
                    enemy.shipY += enemy.speedY #se mueve en y
                    distancia = int(enemy.name) #coef de distancia dependiendo de su nombre, debido a su diferente posicion
                    if enemy.shipY > 0.80: #bajan los enemies
                        enemy.speedX = 0
                        enemy.speedY = -0.0015
                    if enemy.shipY > 0.70 and enemy.shipY < 0.80: #bajan un poco más para entrar en el loop
                        enemy.speedX = 0.0007
                        enemy.speedY = -0.0003
                    if enemy.shipX > (-0.6 + 0.6*(distancia-1) + 0.25): #se mueven a la derecha 
                        enemy.speedX = -0.0007
                        enemy.speedY = 0
                    if enemy.shipX < (-0.6 + 0.6*(distancia-1) -0.25): #se mueven a la izquierda
                        enemy.speedX = 0.0007
                        enemy.speedY = 0
                    #esto fue el loop de movimiento 

                    # disparo de nuestros enemies
                    if int(glfw.get_time()%5)==0:
                        enemy.shoot = True

                    #condicion para que disparen los enemies  
                    if enemy.shoot == True and enemy.bulletY > -1: #que la bullet esté efectivamente en la escena 
                        #Movimiento bullet
                        enemy.bulletY -= enemyBullet.speed # le restamos esto para trasladarla 
                        enemyBulletNode = enemyBullet.get_bullet()
                        enemyBulletNode.transform = tr.matmul([tr.translate(enemy.bulletX,enemy.bulletY,0),tr.scale(0.1,0.2,1)])
                        sg.drawSceneGraphNode(enemyBulletNode, pipelineTexture, "transform") # dibujamos la bullet

                    # condiciones de las bullets para que desaparezcan si impactan o salen de escena 
                    if enemy.bulletY < -1:
                        enemy.shoot = False
                    if enemy.shoot == False: #reseteamos la bullet cuando no se está disparando (volver a su posicion en la escena) 
                        enemy.bulletY = enemy.shipY
                        enemy.bulletX = enemy.shipX
                        enemyBulletNode = enemyBullet.get_bullet()
                        enemyBulletNode.transform = tr.matmul([tr.translate(enemy.shipX,enemy.shipY,0),tr.scale(0.1,0.2,1)])
                    
                    #condicion de impacto de la bullet enemiga con nuestra ship 
                    if hit.hitmarker(enemy.bulletX,enemy.bulletY,controller.shipX,controller.shipY):
                        enemy.shoot = False
                        enemy.bulletY = enemy.shipY
                        enemy.bulletX = enemy.shipX
                        enemyBulletNode = enemyBullet.get_bullet()
                        enemyBulletNode.transform = tr.matmul([tr.translate(enemy.shipX,enemy.shipY,0),tr.scale(0.1,0.2,1)])
                        # nos quita vida 
                        ship.hp -= 1
                    
                    #condicion de impacto de la bullet con ship enemiga 
                    if hit.hitmarker(controller.bulletX,controller.bulletY,enemy.shipX,enemy.shipY):
                        controller.shoot = False
                        enemy.hp -= 1 #le quitamos vida 
                        enemies -= 1 #restamos uno a los enemies totales 
                        if remaining_enemies > 0: #si faltan enemies hacemos un respawn de la ship 
                            remaining_enemies -= 1 #bajamos la cantidad de remaining_enemies 
                            enemy.hp = 1 #revivimos 
                            enemy.shipX = -0.6 + (int(enemy.name)-1)*0.6 #la movemos a su posicion inicial 
                            enemy.shipY = 1.5 

            #############################################################################################################
            #Drawing bullets
            #la condicion para que nuestra ship dispare  
            if controller.shoot == True and controller.bulletY < 1.5: 
                # Movimiento bullet
                controller.bulletY += bullet.speed
                bulletNode = bullet.get_bullet()
                bulletNode.transform = tr.matmul([tr.translate(controller.bulletX,controller.bulletY,0),tr.scale(0.1,0.2,1)])
                sg.drawSceneGraphNode(bulletNode, pipelineTexture, "transform")
            
            #si sale de escena se deja de disparar, para poder resetear la bullet 
            if controller.bulletY > 1.5:
                controller.shoot = False
            if controller.shoot == False: # si es false el shoot reseteamos la bullet a la posicion de nuestra ship 
                controller.bulletY = controller.shipY
                controller.bulletX = controller.shipX
                bulletNode = bullet.get_bullet()
                bulletNode.transform = tr.matmul([tr.translate(controller.shipX,controller.shipY,0),tr.scale(0.1,0.2,1)])
        
        #condicicion de game over, nos sacaron toda la hp
        if ship.hp == 0:
            glUniformMatrix4fv(glGetUniformLocation(pipelineTexture.shaderProgram, "transform"),1,GL_TRUE,tr.scale(1.5,1.5,1))
            if int(glfw.get_time()%2) == 0:
                pipelineTexture.drawShape(gpuGame_over)  
        #condicion de victoria, derrotamos a todos los enemies 
        if enemies == 0: 
            glUniformMatrix4fv(glGetUniformLocation(pipelineTexture.shaderProgram, "transform"),1,GL_TRUE,tr.matmul([tr.translate(0,0.25,0),tr.scale(1.5,1.5,1)]))
            if int(glfw.get_time()%2) != 0:
                pipelineTexture.drawShape(gpuYou_win)  

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
        # actualizamos el t0
        t0 = glfw.get_time()
        
    glfw.terminate()