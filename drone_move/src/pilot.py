#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import quadrotor_traj_main1 as quad
import rospy
import rotational_matrix as rot
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
pub_pilot = rospy.Publisher('bebop/cmd_vel', Twist, queue_size=10)
pub_take_off = rospy.Publisher('bebop/takeoff', Empty, queue_size=10)
pub_land = rospy.Publisher('bebop/land', Empty, queue_size=10)
pub_emergency = rospy.Publisher('bebop/reset', Empty, queue_size=10)
take_off = Empty()
land = Empty()
emergency = Empty()
msg = 'Please Enter the following keys to move the drone\n'
twist = Twist()
settings = termios.tcgetattr(sys.stdin)
x,y = rot.roll_pitch()
try:
    print msg
    while(1):
        key = getKey()
        if key == 'w' :
            twist.linear.x +=.5 
        elif key == 'x' :
            twist.linear.x -=.5 
        elif key == 'a' :
            twist.linear.y +=.5
        elif key == 'd' :
            twist.linear.y -=.5
        elif key == 'r' :
            twist.linear.z +=.5
        elif key == 'f' :
            twist.linear.z -=.5
        elif key == 'o' :
            twist.linear.z +=.5
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
                twist.linear.y = x[i]/.4
                twist.linear.x = y[i]/.411
                twist.linear.z = 0
                pub_pilot.publish(twist)
                rospy.sleep(0.025)
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
