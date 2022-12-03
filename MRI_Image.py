import numpy as np
import matplotlib.pyplot as plt
from math import pow
from phantominator import shepp_logan

TR = 300
TE = 3000

def calculateSI(water, T1, T2star):
    return water * (1 - np.exp(-1 * TR / T1)) * np.exp(-1 * TE / T2star)

def createPhantom(N1, N2, SIA, B, C, maxSI):
    MyPhantom = np.full((N1, N2), SIA)
    plt.figure()
    
    for i in range(N1):
        for j in range(N2):
            if (i, j) in B.keys() and (i, j) in C.keys():
                MyPhantom[i][j] = (B[(i, j)] + C[(i, j)]) / 2
            elif (i, j) in B.keys():
                MyPhantom[i][j] = B[(i, j)]
            elif (i, j) in C.keys():
                MyPhantom[i][j] = C[(i, j)]
            
    plt.imshow(MyPhantom, cmap='gray', vmin=SIA, vmax=maxSI)
    plt.show()  
    
def createRectangle(rParam):
    SI = calculateSI(rParam["water"], rParam["T1"], rParam["T2star"])
    map = {}
    
    for i in range(rParam["PosB1"], rParam["PosB1"] + rParam["LengthB1"]):
        for j in range(rParam["PosB2"], rParam["PosB2"] + rParam["LengthB2"]):
            map[(i,j)] = SI        
    return map
    
def createEllipse(eParam):
    SI = calculateSI(eParam["water"], eParam["T1"], eParam["T2star"])
    map = {}
    
    for i in range(eParam["PosC1"] - eParam["LengthC2"], eParam["PosC1"] + eParam["LengthC1"]):
        for j in range(eParam["PosC2"] - eParam["LengthC2"], eParam["PosC2"] + eParam["LengthC2"]):
            if (pow(i - eParam["PosC1"], 2) / pow(eParam["LengthC1"]/2, 2) + pow(j - eParam["PosC2"], 2) / pow(eParam["LengthC2"]/2, 2)) < 1: 
                map[(i,j)] = SI        
    return map
            
def main():
    N1, N2 = 100, 100
    SIA = calculateSI(0, 5, 5)
    maxSI = 256
    
    rectangleParameters = {
        "PosB1": 40, 
        "PosB2": 20,
        "LengthB1": 30,
        "LengthB2": 30,
        "water": 220,
        "T1": 1500,
        "T2star": 100
    }
    B = createRectangle(rectangleParameters)
    
    ellipseParameters = {
        "PosC1": 70, 
        "PosC2": 70,
        "LengthC1": 30,
        "LengthC2": 20,
        "water": 50,
        "T1": 200,
        "T2star": 10 
    }
    C = createEllipse(ellipseParameters)
    
    createPhantom(N1, N2, SIA, B, C, maxSI)
  
if __name__=="__main__":
    main()