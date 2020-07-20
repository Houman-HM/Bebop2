#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import traj_generation as traj
import rospy
import numpy as np
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

rospy.init_node('drone_teleop')
pub_pilot = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
pub_take_off = rospy.Publisher('ardrone/takeoff', Empty, queue_size=10)
pub_land = rospy.Publisher('ardrone/land', Empty, queue_size=10)
pub_emergency = rospy.Publisher('ardrone/reset', Empty, queue_size=10)
take_off = Empty()
land = Empty()
emergency = Empty()
msg = 'Please Enter the following keys to move the drone\n'
twist = Twist()
settings = termios.tcgetattr(sys.stdin)
x,y = traj.traj_quadrotor_comp()
try:
    print (msg)
    while(1):
        key = getKey()
        if key == 'w' :
            twist.linear.x +=1 
        elif key == 'x' :
            twist.linear.x -=1 
        elif key == 'a' :
            twist.linear.y +=1 
        elif key == 'd' :
            twist.linear.y -=1 
        elif key == 'r' :
            twist.linear.z +=1
        elif key == 'f' :
            twist.linear.z -=1
        elif key == 'o' :
            twist.linear.z +=1
        elif key == '1' :
            twist.angular.z +=0.5
        elif key == '3' :
            twist.angular.z -=0.5
        elif key == 't' :
   		    pub_take_off.publish(take_off)
        elif key == 'l' :
   		    pub_land.publish(land)
        elif key == '5' :
   		    pub_emergency.publish(emergency)
        elif key == 'g' :
            counter=0
            for i in range (np.size(x)):
                twist.linear.x = x[i]
                twist.linear.y = y[i]
                twist.linear.z = 0
                pub_pilot.publish(twist)
                rospy.sleep(0.02)
                counter+=1
                if (counter>np.size(x)-1):
                    twist.linear.x = 0
                    twist.linear.y = 0
                    twist.linear.z = 0
                    pub_pilot.publish(twist)
                    break

        elif key == ' ' or key == 's' :
            twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        else:
            if (key == '\x03'):
                break

        pub_pilot.publish(twist)
finally:
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub_pilot.publish(twist)
