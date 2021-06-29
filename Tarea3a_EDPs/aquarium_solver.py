# coding=utf-8
"""
Sebastián Salinas, CC3501-Tarea3a, 2020-1
Finite Differences for Partial Differential Equations

Solving the Laplace equation in 3D with Dirichlet and
Neumann border conditions over a parallelepiped domain.
"""
import numpy as np
import sys
import json_reader as r
import scipy.sparse as sparse
import scipy.sparse.linalg as linalg
import matplotlib.pyplot as plt

# Input
problem_setup_name = sys.argv[1] # Problem setup file
problem_setup_dict = r.jsonToDict(problem_setup_name) # Dictonary for the problem setup constants

# Problem setup
H = problem_setup_dict["height"]
W = problem_setup_dict["width"]
L = problem_setup_dict["lenght"]

# Paso de discretización 
h = 0.1 # 0.125

# Neumann conditions:
F = problem_setup_dict["window_loss"]  #at right, left, far and near

# Boundary Dirichlet Conditions:
heater_a = problem_setup_dict["heater_a"]
heater_b = problem_setup_dict["heater_b"]
T = problem_setup_dict["ambient_temperature"]
fileName = problem_setup_dict["filename"]

# Path
path = "Solutions/"

# Number of unknowns
# Only the top side and the heaters at the bottom are known (Dirichlet condition)
# right, left, far and near are unknown (Neumann condition)
nx = int(W / h) + 1
ny = int(L / h) + 1
nz = int(H / h)

# In this case, the domain is an aquarium with parallelepiped form
N = nx * ny * nz

# We define a function to convert the indices from i,j,k to P and viceversa
# i,j,k indexes the discrete domain in 3D.
# P parametrize those i,j,k this way we can tidy the unknowns
# in a column vector and use the standard algebra

def getP(i,j,k):
    return k*(nx*ny) + j*nx + i

def getIJK(P):
    k = P // (nx*ny)
    i = P % nx
    j = (P // nx) -k*ny
    return (i, j, k)

"""
# This code is useful to debug the indexation functions above
print("="*10)
print(getP(0,0,0), getIJK(0))
print(getP(30,50,0), getIJK(1580))
print(getP(30,50,1), getIJK(3161))
print(getP(0,0,2), getIJK(3162))
print("="*10)

import sys
sys.exit(0)
"""

# In this matrix we will write all the coefficients of the unknowns
#A = np.zeros((N,N))
A = sparse.lil_matrix((N,N)) # We use a sparse matrix in order to spare memory, since it has many 0's

# In this vector we will write all the right side of the equations
b = np.zeros((N,))

# Note: To write an equation is equivalent to write a row in the matrix system

# We iterate over each point inside the domain
# Each point has an equation associated
# The equation is different depending on the point location inside the domain
for k in range(0, nz):
    for j in range(0, ny):
        for i in range(0, nx):
            # We will write the equation associated with row P
            P = getP(i, j, k)
            # We obtain indices of the other coefficients
            P_right = getP(i+1, j, k)
            P_left = getP(i-1, j, k)
            P_far = getP(i, j+1, k)
            P_near = getP(i, j-1, k)
            P_up = getP(i, j, k+1)
            P_down = getP(i, j, k-1)
            
            # Depending on the location of the point, the equation is different:

            # Interior
            if (1 <= i) and (i <= nx - 2) and (1 <= j) and (j <= ny - 2) and (1 <= k) and (k <= nz-2):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(1))
                A[P, P_right] = 1
                A[P, P_left] = 1
                A[P, P_far] = 1
                A[P, P_near] = 1
                A[P, P_up] = 1
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = 0
     
            # Right 
            elif i == nx-1 and (1 <= j) and (j <= ny - 2) and (1 <= k) and (k <= nz-2):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(2))
                A[P, P_left] = 2
                A[P, P_far] = 1
                A[P, P_near] = 1
                A[P, P_up] = 1
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -2 * h * F

            # Left 
            elif i == 0 and (1 <= j) and (j <= ny - 2) and (1 <= k) and (k <= nz-2):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(3))
                A[P, P_right] = 2
                A[P, P_far] = 1
                A[P, P_near] = 1
                A[P, P_up] = 1
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -2 * h * F
            
            # Far 
            elif (1 <= i) and (i <= nx-2) and j == ny-1 and (1 <= k) and (k <= nz-2):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(4))
                A[P, P_right] = 1
                A[P, P_left] = 1
                A[P, P_near] = 2
                A[P, P_up] = 1
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -2 * h * F

            # Near 
            elif (1 <= i) and (i <= nx-2) and j == 0 and (1 <= k) and (k <= nz-2):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(5))
                A[P, P_right] = 1
                A[P, P_left] = 1
                A[P, P_far] = 2
                A[P, P_up] = 1
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -2 * h * F
    
            # Top 
            elif (1 <= i) and (i <= nx - 2) and (1 <= j) and (j <= ny-2) and k == nz-1:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(6))
                A[P, P_right] = 1
                A[P, P_left] = 1
                A[P, P_far] = 1
                A[P, P_near] = 1
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -T

            # heater_a
            elif (nx//3 <= i) and (i <= 2*nx//3) and (3*ny//5 <= j) and (j <= 4*ny//5) and k == 0:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(8))
                A[P, P_right] = 0
                A[P, P_left] = 0
                A[P, P_far] = 0
                A[P, P_near] = 0
                A[P, P_up] = 0
                A[P, P] = 1
                b[P] =  heater_a

            # heater_b
            elif (nx//3 <= i) and (i <= 2*nx//3) and (ny//5 <= j) and (j <= 2*ny//5) and k == 0:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(9))
                A[P, P_right] = 0
                A[P, P_left] = 0
                A[P, P_far] = 0
                A[P, P_near] = 0
                A[P, P_up] = 0
                A[P, P] = 1
                b[P] =  heater_b

            # Bottom 
            elif (1 <= i) and (i <= nx - 2) and (1 <= j) and (j <= ny-2) and k == 0:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(7))
                A[P, P_right] = 1
                A[P, P_left] = 1
                A[P, P_far] = 1
                A[P, P_near] = 1
                A[P, P_up] = 2
                A[P, P] = -6
                b[P] = 0
            #---------------------------------------------------------------------------------------------------
            # Edges:
            # Right bottom
            elif i == nx-1 and (1 <= j) and (j <= ny - 2) and k == 0:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(10))
                A[P, P_left] = 2
                A[P, P_far] = 1
                A[P, P_near] = 1
                A[P, P_up] = 2
                A[P, P] = -6
                b[P] = -2 * h * F

            # Left bottom 
            elif i == 0 and (1 <= j) and (j <= ny - 2) and k == 0:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(11))
                A[P, P_right] = 2
                A[P, P_far] = 1
                A[P, P_near] = 1
                A[P, P_up] = 2
                A[P, P] = -6
                b[P] = -2 * h * F

            # Far bottom
            elif (1 <= i) and (i <= nx-2) and j == ny-1 and k == 0:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(12))
                A[P, P_right] = 1
                A[P, P_left] = 1
                A[P, P_near] = 2
                A[P, P_up] = 2
                A[P, P] = -6
                b[P] = -2 * h * F

            # Near bottom
            elif (1 <= i) and (i <= nx-2) and j == 0 and k == 0:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(13))
                A[P, P_right] = 1
                A[P, P_left] = 1
                A[P, P_far] = 2
                A[P, P_up] = 2
                A[P, P] = -6
                b[P] = -2 * h * F

            # Right far
            elif i == nx-1 and j == ny-1 and (1 <= k) and (k <= nz-2):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(14))
                A[P, P_left] = 2
                A[P, P_near] = 2
                A[P, P_up] = 1
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -4 * h * F
            
            # Left far
            elif i == 0 and j == ny-1 and (1 <= k) and (k <= nz-2):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(15))
                A[P, P_right] = 2
                A[P, P_near] = 2
                A[P, P_up] = 1
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -4 * h * F
            
            # Right near
            elif i == nx-1 and j == 0 and (1 <= k) and (k <= nz-2):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(16))
                A[P, P_left] = 2
                A[P, P_far] = 2
                A[P, P_up] = 1
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -4 * h * F
            
            # Left near
            elif i == 0 and j == 0 and (1 <= k) and (k <= nz-2):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(17))
                A[P, P_right] = 2
                A[P, P_far] = 2
                A[P, P_up] = 1
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -4 * h * F
            #---------------------------------------------------------------------------------------------------
            # Special case: Almost the corners on the top side
            # Corner right far
            elif i == nx-1 and j == ny-1 and k == nz-1:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(18))
                A[P, P_left] = 2
                A[P, P_near] = 2
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -4 * h * F -T
            
            # Corner left far
            elif i == 0 and j == ny-1 and k == nz-1:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(19))
                A[P, P_right] = 2
                A[P, P_near] = 2
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -4 * h * F -T
            
            # Corner right near
            elif i == nx-1 and j == 0 and k == nz-1:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(20))
                A[P, P_left] = 2
                A[P, P_far] = 2
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -4 * h * F -T
            
            # Corner left near
            elif i == 0 and j == 0 and k == nz-1:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(21))
                A[P, P_right] = 2
                A[P, P_far] = 2
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -4 * h * F -T
            #---------------------------------------------------------------------------------------------------
            # Another special case: The "edge" almost on the top side
            # Right side
            elif i == nx-1 and (1 <= j) and (j <= ny - 2) and k == nz-1:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(22))
                A[P, P_left] = 2
                A[P, P_far] = 1
                A[P, P_near] = 1
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -2 * h * F -T

            # Left side
            elif i == 0 and (1 <= j) and (j <= ny - 2) and k == nz-1:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(23))
                A[P, P_right] = 2
                A[P, P_far] = 1
                A[P, P_near] = 1
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -2 * h * F -T
            
            # Far side
            elif (1 <= i) and (i <= nx-2) and j == ny-1 and k == nz-1:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(24))
                A[P, P_right] = 1
                A[P, P_left] = 1
                A[P, P_near] = 2
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -2 * h * F -T

            # Near side
            elif (1 <= i) and (i <= nx-2) and j == 0 and k == nz-1:
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(25))
                A[P, P_right] = 1
                A[P, P_left] = 1
                A[P, P_far] = 2
                A[P, P_down] = 1
                A[P, P] = -6
                b[P] = -2 * h * F -T
            #-----------------------------------------------------
            # Bottom corners:
            # Corner bottom far right
            elif (i, j, k) == (nx-1,ny-1,0):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(26))
                A[P, P_left] = 2
                A[P, P_near] = 2
                A[P, P_up] = 2
                A[P, P] = -6
                b[P] = -4 * h * F

            # Corner bottom far left
            elif (i, j, k) == (0,ny-1,0):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(27))
                A[P, P_right] = 2
                A[P, P_near] = 2
                A[P, P_up] = 2
                A[P, P] = -6
                b[P] = -4 * h * F

            # Corner bottom near right
            elif (i, j, k) == (nx-1,0,0):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(28))
                A[P, P_left] = 2
                A[P, P_far] = 2
                A[P, P_up] = 2
                A[P, P] = -6
                b[P] = -4 * h * F

            # Corner bottom near left
            elif (i, j, k) == (0,0,0):
                #print("(",str(i)," ",str(j), " ",str(k),")"," ",str(29))
                A[P, P_right] = 2
                A[P, P_far] = 2
                A[P, P_up] = 2
                A[P, P] = -6
                b[P] = -4 * h * F

            else:
                print("Point (" + str(i) + ", " + str(j) + ", " + str(k) + ") missed!")
                print("Associated point index is " + str(P))
                raise Exception()


# A quick view of a sparse matrix
#plt.spy(A)

# Solving our system
#x = np.linalg.solve(A, b)
x = linalg.spsolve(A, b)

# Now we return our solution to the 3d discrete domain:

u = np.zeros((nx,ny,nz)) # In this matrix we will store the solution in the 3d domain

for P in range(0, N):
    i,j,k = getIJK(P)
    u[i,j,k] = x[P]      # LLenamos la matriz con la solución  

# Adding the borders, as they have known values
ub = np.zeros((nx,ny,nz+1))
ub[0:nx, 0:ny, 0:nz] = u[:,:,:]

# Dirichlet boundary condition on the top side
ub[0:nx, 0:ny, nz] = T

# Saving results for temperatures
np.save(path + fileName,ub)

# Visualization:
# this visualization locates the (0,0,0) at the lower left corner

#limites: (W/h)+1, (L/h)+1 y (H/h)+1
#-> Ejemplo, h=1 se tiene que (W/h)+1 = 4, (L/h)+1 = 7 y (H/h)+1 = 5
#h=0.5 -> 7,13,9
#h=0.2 -> 16,31,21
#h=0.1 -> 31,61,41
W_limit=int((W/h)+1)
L_limit=int((L/h)+1) 
H_limit=int((H/h)+1)

# Grillado
#X_prima, Y_prima, Z_prima = np.mgrid[0:W:16j, 0:L:31j, 0:H:21j]
# Equivalentemente:
Y, X, Z = np.meshgrid(np.linspace(0, L, L_limit),np.linspace(0,W,W_limit),np.linspace(0,H,H_limit))

"""
# Para debugear y ver que son equivalentes:
Y_prima,X_prima,Z_prima = np.meshgrid(np.linspace(0, L, 7),np.linspace(0,W,4),np.linspace(0,H,5))
if X.all()==X_prima.all():
    print("True")
if Y.all()==Y_prima.all():
    print("True")
if Z.all()==Z_prima.all():
    print("True")
"""

fig = plt.figure()
ax = fig.gca(projection='3d')

scat = ax.scatter(X,Y,Z, c=ub, alpha=0.5, s=100, marker='s', edgecolors="k")

fig.colorbar(scat, shrink=0.5, aspect=5) # This is the colorbar at the side

# Showing the result
ax.set_title('Laplace equation solution from aquarium')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()

# Note:
# imshow is also valid but it uses another coordinate system,
# a data transformation is required
#ax.imshow(ub.T)

