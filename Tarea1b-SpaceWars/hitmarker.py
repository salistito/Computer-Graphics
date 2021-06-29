"""
Sebastián Salinas, CC3501, 6/05/20
Tarea1b
"""
# Importamos algunos modulos
import math
# Función para evaluar la colisión entre 2 objetos
def hitmarker(x1,y1,x2,y2):
    distancia = math.sqrt((x1-x2)**2 + (y1-y2)**2) # Ecuación de la distancia
    if distancia < 0.075: #0.075
        return True
    else:
        return False