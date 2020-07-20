#!/usr/bin/env python
import rospy
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sc
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios
def getKey():
  if os.name == 'nt':
    return msvcrt.getch()

  tty.setraw(sys.stdin.fileno())
  rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
  if rlist:
      key = sys.stdin.read(1)
  else:
      key = ''

  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
  return key
settings = termios.tcgetattr(sys.stdin)

x = []
y= []
z= []
def callback(data):
  x.append(data.pose.pose.position.x)
  y.append(data.pose.pose.position.y)
  
  z.append(data.pose.pose.position.z)

rospy.init_node('read_joints', anonymous=True)
rospy.Subscriber("/bebop/odom", Odometry, callback)
# print ('here I am')
# nx = np.array((joint0,joint1,joint2,joint3,joint4,joint5,joint6))
# adict = {}
# adict['nx'] = nx
# sc.savemat('file.mat',adict)
# pd.DataFrame({'joint0': joint0, 'joint1': joint1, 'joint2':joint2, 'joint3':joint3, 'joint4':joint4, 'joint5':joint5, 'joint6':joint6}).to_csv('file.csv', index=False)
while (1):
  key = getKey()
  if key=='t':
    break
plt.figure(1)
plt.plot(x, y)
plt.show()