from nav_msgs.msg import Odometry
import numpy as np

position = np.zeros((200,3))
orientation = np.zeros((200,4))
counter = 0
def callback(data):
    position[counter][0] = data.position.x
    position[counter][1] = data.position.y
    position[counter][2] = data.position.z
    orientation[counter][0] = data.orientation.x
    orientation[counter][1] = data.orientation.y
    orientation[counter][2] = data.orientation.z
    orientation[counter][3] = data.orientation.w   


while (True)
    rospy.init_node('store_odom', anonymous=True)
    rospy.Subscriber('bebop/odom', Odometry, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()