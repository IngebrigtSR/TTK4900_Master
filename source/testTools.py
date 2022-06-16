#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 09:08:09 2022

@author: ingebrigt
"""

import numpy as np
import matplotlib.pyplot as plt

class Testcircle():
    def makeCurve(amp, offset, delay, res):
        listCurve = np.zeros([res, 1], float)
        delayrad = np.radians(delay)
        for i in range(1, res):
            angle = (i/res)*2*np.pi + delayrad
            point = 30 * np.cos(angle) + offset
            listCurve[i] = point
        return listCurve
            
            
    def makeFig(self, curve1, curve2, curve3):
        figCoordinates = np.zeros((len(curve1), 4))
        for i in range(len(curve1)):
            figCoordinates[i][0] = curve1[i]
            figCoordinates[i][1] = curve2[i]
            figCoordinates[i][2] = curve3[i]
        return figCoordinates
        
def run():
    test = Testcircle()
    res = 100
    testcurve1 = test.makeCurve(90, 0, res)
    testcurve2 = test.makeCurve(90, 120, res)
    testcurve3 = test.makeCurve(90, 240, res)
    print(testcurve1)
    N = np.zeros(res)
                 
    for i in range(1, res):
        N[i] = i
    
    plt.scatter(N, testcurve1)
    #plt.title("Actuator 1")
    plt.xlabel("Testcurve1")
    plt.ylabel("Value")
    plt.show()
    
    plt.scatter(N, testcurve2)
    #plt.title("Actuator 1")
    plt.xlabel("Testcurve2")
    plt.ylabel("Value")
    plt.show()
    
    plt.scatter(N, testcurve3)
    #plt.title("Actuator 1")
    plt.xlabel("Testcurve3")
    plt.ylabel("Value")
    plt.show()

    X, Y, Z = testcurve1, testcurve2, testcurve3
    
    # Plot X,Y,Z
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #ax.plot_trisurf(X, Y, Z, color='white', edgecolors='grey', alpha=0.5)
    #ax.set_title('The lengths of the actuators controlling the direction')
    ax.set_xlabel('$Actuator 1$')
    ax.set_ylabel('$Actuator 2$')
    ax.set_zlabel('$Actuator 3$')
    ax.scatter(X, Y, Z, c='red')
    plt.show()

if __name__ == "__main__":
    run()