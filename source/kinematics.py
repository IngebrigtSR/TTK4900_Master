# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 14:51:16 2021

@author: ingebrsr
"""

import numpy as np

class kinematics():
    def __init__(self):
        #Setting parameters and defining values
        #Lengths are in cm
        #Angles in radians
        self.r     = 4.75 #These must be measured properly
        self.R     = 10
        self.psi   = 0 # X, Roll
        self.theta = 0 # Y, pitch 
        self.phi   = 0 # Z, Yaw. Ø i paperet, z-rotasjon, skal være 0
        
        self.camheight = 40
        self.minactuatorlength = 16.8
        self.maxactuatorlength = 26.8
        self.midactuatorlength = (self.minactuatorlength + self.maxactuatorlength)/2
        self.strokelength = 10
        
        self.p_1 = np.array([self.r, 0, 0])
        self.p_2 = np.array([self.r*np.cos(2*np.pi/3), self.r*np.sin(2*np.pi/3), 0])
        self.p_3 = np.array([self.r*np.cos(4*np.pi/3), self.r*np.sin(4*np.pi/3), 0])

        self.p = np.array([self.p_1, self.p_2, self.p_3, [1, 1, 1]]) 
        self.p_e = np.array([self.p_1, self.p_2, self.p_3]) 
        
        self.b_1 = np.array([self.R, 0, 0])
        self.b_2 = np.array([self.R*np.cos(2*np.pi/3), self.R*np.sin(2*np.pi/3), 0])
        self.b_3 = np.array([self.R*np.cos(4*np.pi/3), self.R*np.sin(4*np.pi/3), 0])

        self.b = np.array([self.b_1, self.b_2, self.b_3, [1, 1, 1]])
        self.b_e = np.array([self.b_1, self.b_2, self.b_3])

        self.q = np.array([0, 0, 0]) #Sisteverdien er vel egentlig høyden til mellom platene



    def calcRotation(self, roll, pitch, yaw):
        
        R_p_1 = [np.cos(pitch)*np.cos(yaw), np.cos(pitch)*np.sin(yaw), -np.sin(pitch)]
                       
        R_p_2 = [(np.sin(roll)*np.sin(pitch)*np.cos(yaw) - np.cos(roll)*np.sin(yaw)),
                        (np.sin(roll)*np.sin(pitch)*np.sin(yaw) + np.cos(roll)*np.cos(yaw)),
                        np.cos(pitch)*np.sin(roll)]
                       
        R_p_3 = [(np.cos(roll)*np.sin(pitch)*np.cos(yaw) + np.sin(roll)*np.sin(yaw)),
                        (np.cos(roll)*np.sin(pitch)*np.sin(yaw) - np.sin(roll)*np.cos(yaw)),
                        np.cos(pitch)*np.cos(roll)]
        R_p = [R_p_1, R_p_2, R_p_3]
        return R_p
    
    def calcRotationNome(self, roepos, height):
        x = roepos[0]
        y = roepos[1]
        z = height
        theta = np.arctan(y/x)
        
        
        R_p_Nome = np.array([[np.cos(theta)+x^2*(1-np.cos(theta)), x*y*(1-np.cos(theta))-z*np.sin(theta), x*z*(1-np.cos(theta))+y*np.sin(theta)],
                              [y*x*(1-np.cos(theta))+z*np.sin(theta), np.cos(theta)+y^2*(1-np.cos(theta)),y*z*(1-np.cos(theta))-x*np.sin(theta)],
                              [z*x*(1-np.cos(theta))-y*np.sin(theta),z*y*(1-np.cos(theta))+x*np.sin(theta), np.cos(theta)+z^2*(1-np.cos(theta))]])
        
        return R_p_Nome
    #Eksperimentell løsning fra Morten Andreas Nome
        
    def calcTransform(self, roll, pitch, yaw, q):
        rotation = self.calcRotation(roll, pitch, yaw)
        T_p = np.array([[rotation[0][0], rotation[0][1], rotation[0][2], q[0]],
                       [rotation[1][0], rotation[1][1], rotation[1][2], q[1]],
                       [rotation[2][0], rotation[2][1], rotation[2][2], q[2]],
                       [0, 0, 0, 1]])
        return T_p
    #Muligens noe krøvel her og
    
    def calcLegLength(self, roll, pitch, yaw, q, p, b): 
        P = self.calcTransform(roll, pitch, yaw, self.q) @ self.p
        #P = self.calcRotationNome(roll, pitch, yaw) @ self.p_e
        l_1 = np.sqrt(((P[0][0] - b[0][0])**2) + ((P[0][1] - b[0][1])**2) + ((P[0][2] - b[0][2])**2))
        l_2 = np.sqrt(((P[1][0] - b[1][0])**2) + ((P[1][1] - b[1][1])**2) + ((P[1][2] - b[1][2])**2))
        l_3 = np.sqrt(((P[2][0] - b[2][0])**2) + ((P[2][1] - b[2][1])**2) + ((P[2][2] - b[2][2])**2))
        
        l_1 = ((self.minactuatorlength - l_1) / self.strokelength)
        l_2 = ((self.minactuatorlength - l_2) / self.strokelength)
        l_3 = ((self.minactuatorlength - l_3) / self.strokelength)
        
        #AVG Normalisering
        avg = (l_1 + l_2 + l_3) / 3
        adj = 1 - avg
        l_1 = (l_1 + adj)*90
        l_2 = (l_2 + adj)*90
        l_3 = (l_3 + adj)*90
        l = np.array([l_1, l_2, l_3])
        return l
    #Eksperimentelt
    
    
    def fourthActuator(self, roll, pitch, yaw, q, p, dis):
        P = self.calcTransform(roll, pitch, 0, self.q) @ self.p
        P2 = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, dis],
                        [0, 0, 0, 1]]) @ P
        l_4 = (np.sqrt((P2[2][2] - P[2][2])**2) / self.strokelength)*90
        return l_4
    
    def listLegLengths(self, dirdislist):
        listleglengths = np.zeros((len(dirdislist), 4))
        for i in range(len(listleglengths)):
            roll = dirdislist[i][0]
            pitch = dirdislist[i][1]
            dis = dirdislist[i][2]
            
            l = self.calcLegLength(roll, pitch, 0, self.q, self.p, self.b)
            
            l_4 = self.fourthActuator(roll, pitch, 0, self.q, self.p, dis)
            
            leglength = [l[0], l[1], l[2], l_4]
            
            listleglengths[i] = leglength
            
        return listleglengths
    
    # def positionFromActuatorLengths(self, actuators):
        
    #     dirActuators = actuators[:, [0, 1, 2]]
    #     dis = actuators[:, 3]
    #     pos = np.zeros(len(dis), 3)
        
    #     for i in range(len(dis)):
            
        
    #     for i in range(len(dis)):
    #         diractuators
    
    # def calcWorkspace(self, ):
        #lag et array med alle mulige actuatorlengder oppløsning 0.1


def run():
    kin = kinematics()
    #transform = kin.calcTransform(30, 60, 45, kin.q)
    leglength = kin.calcLegLength(30, 60, 45, kin.q, kin.p, kin.b)
    #rotation= kin.calcRotation(0, 0, 0)
    
    print(leglength)
    
    print("Run complete")


if __name__ == "__main__":
    run()