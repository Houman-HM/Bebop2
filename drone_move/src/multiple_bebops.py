#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import rospy
import numpy as np
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios
  
from scipy.io import loadmat
import matplotlib.pyplot as plt




pitch_temp = loadmat('pitch_leader.mat')
pitch_robot_1 = pitch_temp['pitch_quad'].squeeze()

roll_temp = loadmat('roll_leader.mat')
roll_robot_1 = roll_temp['roll_quad'].squeeze()

pitch_temp = loadmat('pitch_leader.mat')
pitch_robot_2 = pitch_temp['pitch_quad'].squeeze()

roll_temp = loadmat('roll_leader.mat')
roll_robot_2 = roll_temp['roll_quad'].squeeze()

vx_traj_temp = loadmat('xdot_rob_dyn_singleobs')
vx_robot_1 = vx_traj_temp['xdot'].squeeze()


vy_traj_temp = loadmat('ydot_rob_dyn_singleobs')
vy_robot_1 = vy_traj_temp['ydot'].squeeze()

vx_traj_temp = loadmat('vx_robot_2.mat')
vx_robot_2 = vx_traj_temp['vx_quad'].squeeze()

vy_traj_temp = loadmat('vy_robot_2.mat')
vy_robot_2 = vy_traj_temp['vy_quad'].squeeze()

print roll_robot_2
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

rospy.init_node('drone_teleop', anonymous=True, disable_signals=True)
bebop1_pilot = rospy.Publisher('bebop1/velocity', Twist, queue_size=10)
bebop2_pilot = rospy.Publisher('bebop2/velocity', Twist, queue_size=10)
bebop1_take_off = rospy.Publisher('bebop1/takeoff', Empty, queue_size=10)
bebop1_land = rospy.Publisher('bebop1/land', Empty, queue_size=10)
bebop2_take_off = rospy.Publisher('bebop2/takeoff', Empty, queue_size=10)
bebop2_land = rospy.Publisher('bebop2/land', Empty, queue_size=10)
bebop1_emergency = rospy.Publisher('bebop1/reset', Empty, queue_size=10)
bebop2_emergency = rospy.Publisher('bebop2/reset', Empty, queue_size=10)


take_off = Empty()
land = Empty()
emergency = Empty()
msg = 'Please Enter the following keys to move the drone\n'
twist_1 = Twist()
twist_2 = Twist()
settings = termios.tcgetattr(sys.stdin)
try:
    print (msg)
    while(1):
        key = getKey()
        if key == 'w' :
            twist_1.linear.x +=1
            bebop1_pilot.publish(twist_1)
        elif key == 'x' :
            twist_1.linear.x -=1 
            bebop1_pilot.publish(twist_1)
        elif key == 'a' :
            twist_1.linear.y +=1 
            bebop1_pilot.publish(twist_1)
        elif key == 'd' :
            twist_1.linear.y -=1
            bebop1_pilot.publish(twist_1)
        elif key == 'r' :
            twist_1.linear.z +=1
            bebop1_pilot.publish(twist_1)
            bebop2_pilot.publish(twist_1)
        elif key == 'f' :
            twist_1.linear.z -=1
            bebop1_pilot.publish(twist_1)
        elif key == 'o' :
            twist_1.linear.z +=1
            bebop1_pilot.publish(twist_1)
        elif key == '1' :
            twist_1.angular.z +=0.5
            bebop1_pilot.publish(twist_1)
        elif key == '3' :
            twist_1.angular.z -=0.5
            bebop1_pilot.publish(twist_1)
        elif key == 't' :
   		    bebop1_take_off.publish(take_off)
   		    bebop2_take_off.publish(take_off)
        elif key == 'l' :
            bebop1_land.publish(land)
            bebop2_land.publish(land)

        elif key == '5' :
   		    bebop1_emergency.publish(emergency)
   		    bebop2_emergency.publish(emergency)
        elif key == 'g' :
            counter=0
	    print np.size(vy_robot_1)
            for i in range (np.size(vy_robot_1)):
                twist_1.linear.x = vx_robot_1[i]	
                twist_1.linear.y = vy_robot_1[i]
                twist_1.linear.z = 0
                twist_2.linear.x = 0.833#vx_robot_2[i]
                twist_2.linear.y = 0#vy_robot_2[i]
                twist_2.linear.z = 0
                bebop1_pilot.publish(twist_1)
                bebop2_pilot.publish(twist_2)
                rospy.sleep(0.02)
                counter+=1
		print counter
                if (counter>np.size(roll_robot_1)-1):
                    twist_1.linear.x = 0
                    twist_1.linear.y = 0
                    twist_1.linear.z = 0
                    twist_2.linear.x = 0
                    twist_2.linear.y = 0
                    twist_2.linear.z = 0
                    bebop1_pilot.publish(twist_1)
                    bebop2_pilot.publish(twist_2)

                    break

        elif key == ' ' or key == 's' :
            twist_1.linear.x = 0
            twist_1.linear.y = 0
            twist_1.linear.z = 0
            twist_2.linear.x = 0
            twist_2.linear.y = 0
            twist_2.linear.z = 0
            bebop1_pilot.publish(twist_1)
            bebop2_pilot.publish(twist_2)
        else:
            if (key == '\x03'):
                break
except KeyboardInterrupt:
       bebop1_land.publish(land)
       bebop2_land.publish(land)
finally:
	bebop1_land.publish(land)
	bebop2_land.publish(land)
