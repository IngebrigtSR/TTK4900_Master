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

if __name__ == '__main__':
    
    test = detector()
    
    # img = cv2.imread('img00472.png', cv2.IMREAD_GRAYSCALE)

    # results = test.doPredictions(img, [0,1280,0,1024], 0)
    # mid = test.findCenter(img, results)
    # pos = test.makeCartesianList(img, mid)
    
    # img2 = cv2.imread('pseudorogn.jpg', cv2.IMREAD_GRAYSCALE)
    
    # resized = cv2.resize(img2, (1280, 1024))
    # results2 = test.doPredictions(resized, [0,1280,0,1024], 0)
    # mid2 = test.findCenter(resized, results2)
    # pos2 = test.makeCartesianList(resized, mid2)
    # dirdis2 = test.makeDirectionDistanceList(pos2, 10)
    
    # print(mid)
    # print(pos)
    # print(mid2)
    # print(pos2)
    # print(dirdis2)
    
    testkin = kinematics()
    
    # actuatorpostest = np.zeros((len(dirdis2), 3))
    
    # for i in len(len(dirdis2)):
    #     roll = dirdis2[0][0]
    #     pitch = dirdis2[0][1]
    #     dis = dirdis2[0][2]
    #     leglength = testkin.calcLegLength(roll, pitch, 0, [0, 0, dis], testkin.p, testkin.b)
    #     actuatorpostest[i] = leglength
    
    # print(actuatorpostest)
    squareorbit = np.array([[7.5, 7.5],
                            [7.5, 6.5],
                            [7.5, 5.5],
                            [7.5, 4.5],
                            [7.5, 3.5],
                            [7.5, 2.5],
                            [7.5, 1.5],
                            [7.5, 0.5],
                            [7.5, -0.5],
                            [7.5, -1.5],
                            [7.5, -2.5],
                            [7.5, -3.5],
                            [7.5, -4.5],
                            [7.5, -5.5],
                            [7.5, -6.5],
                            [7.5, -7.5],
                            [6.5, -7.5],
                            [5.5, -7.5],
                            [4.5, -7.5],
                            [3.5, -7.5],
                            [2.5, -7.5],
                            [1.5, -7.5],
                            [0.5, -7.5],
                            [-0.5, -7.5],
                            [-1.5, -7.5],
                            [-2.5, -7.5],
                            [-3.5, -7.5],
                            [-4.5, -7.5],
                            [-5.5, -7.5],
                            [-6.5, -7.5],
                            [-7.5, -7.5],
                            [-7.5, -6.5],
                            [-7.5, -5.5],
                            [-7.5, -4.5],
                            [-7.5, -3.5],
                            [-7.5, -2.5],
                            [-7.5, -1.5],
                            [-7.5, -0.5],
                            [-7.5, 0.5],
                            [-7.5, 1.5],
                            [-7.5, 2.5],
                            [-7.5, 3.5],
                            [-7.5, 4.5],
                            [-7.5, 5.5],
                            [-7.5, 6.5],
                            [-7.5, 7.5],
                            [-6.5, 7.5],
                            [-5.5, 7.5],
                            [-4.5, 7.5],
                            [-3.5, 7.5],
                            [-2.5, 7.5],
                            [-1.5, 7.5],
                            [-0.5, 7.5],
                            [0.5, 7.5],
                            [1.5, 7.5],
                            [2.5, 7.5],
                            [3.5, 7.5],
                            [4.5, 7.5],
                            [5.5, 7.5],
                            [6.5, 7.5],
                            [7.5, 7.5]])
    
    squaredirdis = test.makeDirectionDistanceList(squareorbit, 10)
    
    squareactuatorlist = testkin.listLegLengths(squaredirdis) 
    #listLegLengths scrambler skålformen gitt av dirdis
    
    print(squareactuatorlist)
    
    plt.scatter(*zip(*squareorbit))
    plt.show()
    
    X, Y, Z = squareactuatorlist[:,0], squareactuatorlist[:,1], squareactuatorlist[:,2]
    
    # Plot X,Y,Z
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(X, Y, Z, color='white', edgecolors='grey', alpha=0.5)
    ax.scatter(X, Y, Z, c='red')
    plt.show()
    
    serialuno.serialtransmit(squareactuatorlist)
    
    #print(squaredirdis)
    # print(squareactuatorlist)
                   
                   
                   
    
