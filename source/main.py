#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 09:54:49 2022

@author: ingebrigt
"""
import cv2
from roeposition import detector
import preprocessing
import matplotlib.pyplot as plt
from kinematics import kinematics
import numpy as np
import serialuno
import time
import testTools

if __name__ == '__main__':
    
    test = detector()
    
    img = cv2.imread('pseudorogn.jpg', cv2.IMREAD_GRAYSCALE)

    resized = cv2.resize(img, (1280, 1024))
    results = test.doPredictions(resized, [0,1280,0,1024], 0)
    mid = test.findCenter(resized, results)
    pos = test.makeCartesianList(resized, mid)
    
    # img2 = cv2.imread('pseudorogn.jpg', cv2.IMREAD_GRAYSCALE)
    
    
    # results2 = test.doPredictions(resized, [0,1280,0,1024], 0)
    # mid2 = test.findCenter(resized, results2)
    # pos2 = test.makeCartesianList(resized, mid2)
    # dirdis2 = test.makeDirectionDistanceList(pos2, 10)
    pixpos = np.zeros((len(mid), 2))
    for i in range(len(mid)):
        pixpos[i][0] = mid[i][0]
        pixpos[i][1] = mid[i][1]*(-1)
    
    print(mid)
    print(pos)
    
    plt.scatter(*zip(*pixpos))
    # plt.xlim(-15, 20)
    # plt.ylim(-10, 15)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

    
    #testkin = kinematics()
    
    # print(actuatorpostest)
    # squareorbit = np.array([[0, 0],
    #                         [7.5, 7.5],
    #                         [7.5, 6.5],
    #                         [7.5, 5.5],
    #                         [7.5, 4.5],
    #                         [7.5, 3.5],
    #                         [7.5, 2.5],
    #                         [7.5, 1.5],
    #                         [7.5, 0.5],
    #                         [7.5, 0],
    #                         [7.5, -0.5],
    #                         [7.5, -1.5],
    #                         [7.5, -2.5],
    #                         [7.5, -3.5],
    #                         [7.5, -4.5],
    #                         [7.5, -5.5],
    #                         [7.5, -6.5],
    #                         [7.5, -7.5],
    #                         [6.5, -7.5],
    #                         [5.5, -7.5],
    #                         [4.5, -7.5],
    #                         [3.5, -7.5],
    #                         [2.5, -7.5],
    #                         [1.5, -7.5],
    #                         [0.5, -7.5],
    #                         [0, -7.5],
    #                         [-0.5, -7.5],
    #                         [-1.5, -7.5],
    #                         [-2.5, -7.5],
    #                         [-3.5, -7.5],
    #                         [-4.5, -7.5],
    #                         [-5.5, -7.5],
    #                         [-6.5, -7.5],
    #                         [-7.5, -7.5],
    #                         [-7.5, -6.5],
    #                         [-7.5, -5.5],
    #                         [-7.5, -4.5],
    #                         [-7.5, -3.5],
    #                         [-7.5, -2.5],
    #                         [-7.5, -1.5],
    #                         [-7.5, -0.5],
    #                         [-7.5, 0],
    #                         [-7.5, 0.5],
    #                         [-7.5, 1.5],
    #                         [-7.5, 2.5],
    #                         [-7.5, 3.5],
    #                         [-7.5, 4.5],
    #                         [-7.5, 5.5],
    #                         [-7.5, 6.5],
    #                         [-7.5, 7.5],
    #                         [-6.5, 7.5],
    #                         [-5.5, 7.5],
    #                         [-4.5, 7.5],
    #                         [-3.5, 7.5],
    #                         [-2.5, 7.5],
    #                         [-1.5, 7.5],
    #                         [-0.5, 7.5],
    #                         [0, 7.5],
    #                         [0.5, 7.5],
    #                         [1.5, 7.5],
    #                         [2.5, 7.5],
    #                         [3.5, 7.5],
    #                         [4.5, 7.5],
    #                         [5.5, 7.5],
    #                         [6.5, 7.5],
    #                         [7.5, 7.5]
    #                         ])
    
    
    
    # N = np.zeros((len(squareorbit), 1))
    # for i in range(len(squareorbit)):
    #     N[i] = i
    
    # squaredirdis = test.makeDirectionDistanceList(squareorbit, 10)
    
    # #Her har vi hovedmistenkte
    # squareactuatorlist = testkin.listLegLengths(squaredirdis) 
    
    # print(squareactuatorlist)
    
    # plt.scatter(*zip(*squareorbit))
    # #plt.title("A square orbital test route")
    # plt.show()
    
    # X1, Y1, Z1 = squaredirdis[:,0], squaredirdis[:,1], squaredirdis[:,2]
    
    # # Plot X,Y,Z
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_trisurf(X1, Y1, Z1, color='white', edgecolors='grey', alpha=0.5)
    # #ax.set_title('Directions and distances for each point in the square test route')
    # ax.set_xlabel('$Roll$')
    # ax.set_ylabel('$Pitch$')
    # ax.set_zlabel('$Distance$')
    # ax.scatter(X1, Y1, Z1, c='red')
    # plt.show()
    
    # X, Y, Z, W = squareactuatorlist[:,0], squareactuatorlist[:,1], squareactuatorlist[:,2], squareactuatorlist[:,3]
    
    # # Plot X,Y,Z
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_trisurf(X, Y, Z, color='white', edgecolors='grey', alpha=0.5)
    # #ax.set_title('The lengths of the actuators controlling the direction')
    # ax.set_xlabel('$Actuator 1$')
    # ax.set_ylabel('$Actuator 2$')
    # ax.set_zlabel('$Actuator 3$')
    # ax.scatter(X, Y, Z, c='red')
    # plt.show()
    
    # plt.scatter(N, X)
    # #plt.title("Actuator 1")
    # plt.xlabel("Point number")
    # plt.ylabel("Actuator length")
    # plt.show()
    
    # plt.scatter(N, Y)
    # #plt.title("Actuator 2")
    # plt.xlabel("Point number")
    # plt.ylabel("Actuator length")
    # plt.show()
    
    # plt.scatter(N, Z)
    # #plt.title("Actuator 3")
    # plt.xlabel("Point number")
    # plt.ylabel("Actuator length")
    # plt.show()
    
    # plt.scatter(N, W)
    # #plt.title("Actuator 4")
    # plt.xlabel("Point number")
    # plt.ylabel("Actuator length")
    # plt.show()
    
    # circle = testTools.Testcircle()
    
    # res = 60
    # testcurve1 = circle.makeCurve(90, 0, res)
    # testcurve2 = circle.makeCurve(90, 120, res)
    # testcurve3 = circle.makeCurve(90, 240, res)
    
    # testcirclematrix = circle.makeFig(testcurve1, testcurve2, testcurve3)
    
    # with open("leg_lengths.csv") as asquareleglen:
    #     adjustedleglen = np.loadtxt(asquareleglen, delimiter=",")
    
    # adjustedactuatorlist = np.zeros((len(adjustedleglen), 4))
    
    # # for i in range(len(adjustedleglen)):
    # #     adjustedactuatorlist[i] = [adjustedleglen[i][0]*6, adjustedleglen[i][1]*6, adjustedleglen[i][2]*6, 20]
    
    # Xa, Ya, Za, Wa = adjustedactuatorlist[:,0], adjustedactuatorlist[:,1], adjustedactuatorlist[:,2], adjustedactuatorlist[:,3]
    
    # Na = np.zeros((len(adjustedactuatorlist), 1))
    # for i in range(len(adjustedactuatorlist)):
    #     Na[i] = i
        
    # print(adjustedactuatorlist)
    
    # Plot X,Y,Z
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_trisurf(Xa, Ya, Za, color='white', edgecolors='grey', alpha=0.5)
    # #ax.set_title('The lengths of the actuators controlling the direction')
    # ax.set_xlabel('$Actuator 1$')
    # ax.set_ylabel('$Actuator 2$')
    # ax.set_zlabel('$Actuator 3$')
    # ax.scatter(Xa, Ya, Za, c='red')
    # plt.show()
    
    # plt.scatter(Na, Xa)
    # #plt.title("Actuator 1")
    # plt.xlabel("Point number")
    # plt.ylabel("Actuator length")
    # plt.show()
    
    # plt.scatter(Na, Ya)
    # #plt.title("Actuator 2")
    # plt.xlabel("Point number")
    # plt.ylabel("Actuator length")
    # plt.show()
    
    # plt.scatter(Na, Za)
    # #plt.title("Actuator 3")
    # plt.xlabel("Point number")
    # plt.ylabel("Actuator length")
    # plt.show()
    
    # plt.scatter(Na, Wa)
    # #plt.title("Actuator 4")
    # plt.xlabel("Point number")
    # plt.ylabel("Actuator length")
    # plt.show()
    
    # serialuno.serialtransmit(adjustedactuatorlist)

    
    #print(squaredirdis)
    # print(squareactuatorlist)
                   
                   
                   
    
