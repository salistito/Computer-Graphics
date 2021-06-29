import csv
import numpy as np

# Function than coverts a csv file to a python array
def csvToArray(fileName):
    array = []
    with open(fileName) as File:  
        reader = csv.reader(File)
        for row in reader:
            x = float(row[0])
            y = float(row[1])
            z = float(row[2])
            P = np.array([[x,y,z]]).T
            array.append(P)
        return array
