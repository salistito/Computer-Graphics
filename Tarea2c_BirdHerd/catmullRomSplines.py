# coding=utf-8
"""
Sebastián Salinas, CC3501-Tarea2c 
Catmull-Rom splines using python and numpy and matplotlib
"""
import numpy as np
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D

def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T #.T significa transpuesto 


def catmullRomMatrix(P0, P1, P2, P3):
    # Generate a matrix concatenating the columns
    G = np.concatenate((P0, P1, P2, P3), axis=1)

    # Bezier base matrix is a constant
    Mcr = np.array([[0, -1/2, 1, -1/2], [1, 0, -5/2, 3/2], [0, 1/2, 2, -3/2], [0, 0, -1/2, 1/2]])
    
    return np.matmul(G, Mcr)

 
# M is the cubic curve matrix, N is the number of samples between 0 and 1
def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)
    
    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)
    
    for i in range(len(ts)): #Para cada ts genero un vector T 
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T 
        # Recordar que en este caso curve es una matriz de Nx3 (N puntos con sus coordenadas x,y,z)
        
    return curve


def plotCurve(ax, curve, label, color=(0,0,1)): 
    # Recordar que en este caso curve es una matriz de 50x3 (50 puntos con sus coordenadas x,y,z)
    xs = curve[:, 0] #Toda la primera columna
    ys = curve[:, 1] #Toda la segunda columna
    zs = curve[:, 2] #Toda la tercera columna 
    
    ax.plot(xs, ys, zs, label=label, color=color) #ax.plot(xs, ys, zs, "-or") -> linea con puntos y roja

#Los N puntos que definen la curva 
def curvePoints(curve,N):
    points = []
    for i in range(N):
        points.append(curve[i])
    return points

# Función que recibe una matriz de puntos en R^3 transpuestos, para apartir de ahi 
# generar las splines correspondientes y retornar los N puntos que definen ese conjunto de splines
def merchSplinesPoints(pointsList, N=1000):
    largo = len(pointsList)
    trayectoria = []
    for k in range(largo-3):
        GMcr = catmullRomMatrix(pointsList[k], pointsList[k+1], pointsList[k+2], pointsList[k+3])
        catmullRomSpline = evalCurve(GMcr, N)
        points = curvePoints(catmullRomSpline, N)
        trayectoria += points

    return trayectoria


if __name__ == "__main__":    
   
    """
    Example for Catmull-Rom splines
    """

    P0 = np.array([[0, 1, 0]]).T
    P1 = np.array([[0, 1, 1]]).T
    P2 = np.array([[0, 3, 3]]).T
    P3 = np.array([[0, 2, 1]]).T
    
    GMcr = catmullRomMatrix(P0, P1, P2, P3)

    # Number of samples to plot
    N = 50

    catmullRomSpline = evalCurve(GMcr, N)

    points = curvePoints(catmullRomSpline, N)

    # Setting up the matplotlib display for 3D
    fig = mpl.figure()
    ax = fig.gca(projection='3d')
        
    plotCurve(ax, catmullRomSpline, "Catmull-Rom Spline", (1,0,0))
    
    # Adding a visualization of the control points
    controlPoints = np.concatenate((P0, P1, P2, P3), axis=1)
    ax.scatter(controlPoints[0,:], controlPoints[1,:], controlPoints[2,:], color=(1,0,1))


    """
    Example for another Catmull-Rom splines (one step forward)
    """
    
    R0 = np.array([[0, 1, 1]]).T
    R1 = np.array([[0, 3, 3]]).T
    R2 = np.array([[0, 2, 1]]).T
    R3 = np.array([[5, 5, 0]]).T
    
    GMcr2 = catmullRomMatrix(R0, R1, R2, R3)
    catmullRomSpline2= evalCurve(GMcr2, N)

    points2 = curvePoints(catmullRomSpline2, N)
        
    plotCurve(ax, catmullRomSpline2, "Catmull-Rom Spline2", (0,1,0))
    
    # Adding a visualization of the control points
    controlPoints = np.concatenate((R0, R1, R2, R3), axis=1)
    ax.scatter(controlPoints[0,:], controlPoints[1,:], controlPoints[2,:], color=(0,1,1))
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.legend()
    mpl.show()