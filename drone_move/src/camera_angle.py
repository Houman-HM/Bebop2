#!/usr/bin/env python


import rospy
from geometry_msgs.msg import Twist
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
pub = rospy.Publisher('bebop/cmd_vel', Twist, queue_size=10)
msg = 'Please Enter the following keys to move the drone\n'
twist = Twist()
settings = termios.tcgetattr(sys.stdin)

try:
    print msg
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
            
        elif key == ' ' or key == 's' :
            twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        else:
            if (key == '\x03'):
                break

        pub.publish(twist)
finally:
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)
