# A simple class container to store vertices and indices that define a shape
import numpy as np
import basic_shapes as bs

def createColorCube(i, j, k, X, Y, Z, c): # recibe coordenadas i,j,k y los 3 grillados X,Y,Z
    l_x = X[i, j, k]    # Punto (i,j,k) del grillado X
    r_x = X[i+1, j, k]  # Punto (i+1,j,k) del grillado X, me trasladé al siguiente vertices del cubo en el eje x (avance +1)
    b_y = Y[i, j, k]    # Punto (i,j,k) del grillado Y
    f_y = Y[i, j+1, k]  # Punto (i,j+1,k) del grillado Y, me trasladé al siguiente vertices del cubo en el eje y (avance +1)
    b_z = Z[i, j, k]    # Punto (i,j,k) del grillado Z
    t_z = Z[i, j, k+1]  # Punto (i,j,k+1) del grillado Z, me trasladé al siguiente vertices del cubo en el eje z (avance +1)
    
    # Ahora creamos el cubo, igual que en las clases del profe (verlas si no entiendes los vertices e indices para las conexiones)
    
    #   positions    colors
    vertices = [
    # Z+: number 1
        l_x, b_y,  t_z, c[0],c[1],c[2],
         r_x, b_y,  t_z, c[0],c[1],c[2],
         r_x,  f_y,  t_z, c[0],c[1],c[2],
        l_x,  f_y,  t_z, c[0],c[1],c[2],
    # Z-: number 6
        l_x, b_y, b_z, c[0],c[1],c[2],
         r_x, b_y, b_z, c[0],c[1],c[2],
         r_x,  f_y, b_z, c[0],c[1],c[2],
        l_x,  f_y, b_z, c[0],c[1],c[2],
    # X+: number 5
         r_x, b_y, b_z, c[0],c[1],c[2],
         r_x,  f_y, b_z, c[0],c[1],c[2],
         r_x,  f_y,  t_z, c[0],c[1],c[2],
         r_x, b_y,  t_z, c[0],c[1],c[2],
    # X-: number 2
        l_x, b_y, b_z, c[0],c[1],c[2],
        l_x,  f_y, b_z, c[0],c[1],c[2],
        l_x,  f_y,  t_z, c[0],c[1],c[2],
        l_x, b_y,  t_z, c[0],c[1],c[2],
    # Y+: number 4
        l_x,  f_y, b_z, c[0],c[1],c[2],
        r_x,  f_y, b_z, c[0],c[1],c[2],
        r_x,  f_y, t_z, c[0],c[1],c[2],
        l_x,  f_y, t_z, c[0],c[1],c[2],
    # Y-: number 3
        l_x, b_y, b_z, c[0],c[1],c[2],
        r_x, b_y, b_z, c[0],c[1],c[2],
        r_x, b_y, t_z, c[0],c[1],c[2],
        l_x, b_y, t_z, c[0],c[1],c[2],
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return bs.Shape(vertices, indices)


def createRandomColorCube(i, j, k, X, Y, Z): # recibe coordenadas i,j,k y los 3 grillados X,Y,Z
    l_x = X[i, j, k]    # Punto (i,j,k) del grillado X
    r_x = X[i+1, j, k]  # Punto (i+1,j,k) del grillado X, me trasladé al siguiente vertices del cubo en el eje x (avance +1)
    b_y = Y[i, j, k]    # Punto (i,j,k) del grillado Y
    f_y = Y[i, j+1, k]  # Punto (i,j+1,k) del grillado Y, me trasladé al siguiente vertices del cubo en el eje y (avance +1)
    b_z = Z[i, j, k]    # Punto (i,j,k) del grillado Z
    t_z = Z[i, j, k+1]  # Punto (i,j,k+1) del grillado Z, me trasladé al siguiente vertices del cubo en el eje z (avance +1)
    c = np.random.rand  # Para colores randoms, le asignamos un alias a esta función que será llamada muchas veces
    
    # Ahora creamos el cubo, igual que en las clases del profe (verlas si no entiendes los vertices e indices para lasconexiones)
    
    #   positions    colors
    vertices = [
    # Z+: number 1
        l_x, b_y,  t_z, c(),c(),c(),
         r_x, b_y,  t_z, c(),c(),c(),
         r_x,  f_y,  t_z, c(),c(),c(),
        l_x,  f_y,  t_z, c(),c(),c(),
    # Z-: number 6
        l_x, b_y, b_z, 0,0,0,
         r_x, b_y, b_z, 1,1,1,
         r_x,  f_y, b_z, 0,0,0,
        l_x,  f_y, b_z, 1,1,1,
    # X+: number 5
         r_x, b_y, b_z, 0,0,0,
         r_x,  f_y, b_z, 1,1,1,
         r_x,  f_y,  t_z, 0,0,0,
         r_x, b_y,  t_z, 1,1,1,
    # X-: number 2
        l_x, b_y, b_z, 0,0,0,
        l_x,  f_y, b_z, 1,1,1,
        l_x,  f_y,  t_z, 0,0,0,
        l_x, b_y,  t_z, 1,1,1,
    # Y+: number 4
        l_x,  f_y, b_z, 0,0,0,
        r_x,  f_y, b_z, 1,1,1,
        r_x,  f_y, t_z, 0,0,0,
        l_x,  f_y, t_z, 1,1,1,
    # Y-: number 3
        l_x, b_y, b_z, 0,0,0,
        r_x, b_y, b_z, 1,1,1,
        r_x, b_y, t_z, 0,0,0,
        l_x, b_y, t_z, 1,1,1,
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return bs.Shape(vertices, indices)

# Si tenemos 2 shapes, queremos acumular toda esa data en una sola, por lo tanto nos combiene hacer un merge
# de los 2 objetos de la clase shape, y va unir sus vertices e indices (pero los indices son los mismos para ambas del 0 al 7
# por lo cual se hará un offset para "avanzarlos" en 8 y que se puedan diferenciar)

# La función recibe la shape donde quiero que se junten, tamaño del vertice (6, 5 si fueran texturas) y la shape que se unirá
def merge(destinationShape, strideSize, sourceShape): 

    # current vertices are an offset for indices refering to vertices of the new shape
    offset = len(destinationShape.vertices)                                         #24
    destinationShape.vertices += sourceShape.vertices                               #se agregan todos los vertices a una figura
    destinationShape.indices += [(offset/strideSize) + index for index in sourceShape.indices] #24/6 -> 4 + index = 8


def mergeVoxels(X,Y,Z,load_voxels,c,rango=None,delta=None):
    isosurface = bs.Shape([], []) #Cramos una shape a la que le sumaremos cada shape de cubo
    if rango!=None:
        # Now let's draw voxels!
        for i in range(X.shape[0]-1):
            for j in range(X.shape[1]-1):
                for k in range(X.shape[2]-1):
                    # print(X[i,j,k])
                    if load_voxels[i,j,k]>=(rango-delta) and load_voxels[i,j,k]<=(rango+delta):
                        temp_shape = createColorCube(i,j,k, X,Y,Z,c) # Se crea cada cubito
                        merge(destinationShape=isosurface, strideSize=6, sourceShape=temp_shape) # IMPORTANTE: SE FUSIONA EN UNA SOLA
        return isosurface

    else: 
        # Now let's draw voxels!
        for i in range(X.shape[0]-1):
            for j in range(X.shape[1]-1):
                for k in range(X.shape[2]-1):
                    # print(X[i,j,k])
                    if load_voxels[i,j,k]:
                        temp_shape = createColorCube(i,j,k, X,Y,Z,c) # Se crea cada cubito
                        merge(destinationShape=isosurface, strideSize=6, sourceShape=temp_shape) # IMPORTANTE: SE FUSIONA EN UNA SOLA
        return isosurface


def mergeRandomColorVoxels(X,Y,Z,load_voxels,rango=None,delta=None):
    isosurface = bs.Shape([], []) # Creamos una shape a la que le sumaremos cada shape de cubo
    if rango!=None:
        # Now let's draw voxels!
        for i in range(X.shape[0]-1):
            for j in range(X.shape[1]-1):
                for k in range(X.shape[2]-1):
                    # print(X[i,j,k])
                    if load_voxels[i,j,k]>=(rango-delta) and load_voxels[i,j,k]<=(rango+delta):
                        temp_shape = createRandomColorCube(i,j,k, X,Y,Z) # Se crea cada cubito
                        merge(destinationShape=isosurface, strideSize=6, sourceShape=temp_shape) # IMPORTANTE: SE FUSIONA EN UNA SOLA
        return isosurface

    else: 
        # Now let's draw voxels!
        for i in range(X.shape[0]-1):
            for j in range(X.shape[1]-1):
                for k in range(X.shape[2]-1):
                    # print(X[i,j,k])
                    if load_voxels[i,j,k]:
                        temp_shape = createRandomColorCube(i,j,k, X,Y,Z) # Se crea cada cubito
                        merge(destinationShape=isosurface, strideSize=6, sourceShape=temp_shape) # IMPORTANTE: SE FUSIONA EN UNA SOLA
        return isosurface