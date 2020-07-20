#!/usr/bin/env python
from __future__ import division
import quadrotor_traj_main1 as quad
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.linalg import block_diag

# roll= pitch= yaw = []

def rotationMatrixToEulerAngles(R) :
 
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
     
    singular = sy < 1e-6
 
    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
 
    return np.array([x, y, z])
def roll_pitch ():
    xddot, yddot = quad.compute()
    fd = np.ones((200, 3))
    for i in range (200):
        fd[i][0] = xddot[i]
        fd[i][1] = yddot[i]
        fd[i][2] = 10

    r3  = fd/np.linalg.norm(fd)
    r2c = np.ones((200,3))
    r1 = np.ones((200,3))
    r2 = np.ones((200,3))
    roll = np.zeros(200)
    pitch = np.zeros(200)
    yaw = np.zeros(200)
    for i in range (200):
        r2c[i][0] =0
        r2c[i][1] = 1
        r2c[i][2] = 0
    for i in range (200):
        r1[i] =  np.cross(r2c[i],r3[i])/np.linalg.norm(np.cross(r2c[i],r3[i]))
        r2[i] = np.cross(r3[i],r1[i])
        R = np.vstack((r1[i],r2[i],r3[i])).T
        roll[i],pitch[i],yaw[i] = rotationMatrixToEulerAngles(R)
    return roll, pitch
    # roll.append(x)
    # pitch.append(y)
    # yaw.append(z)


# x,y,z  = rotationMatrixToEulerAngles(R)
#print (isRotationMatrix(R))
