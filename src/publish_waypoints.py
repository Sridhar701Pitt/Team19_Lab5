#!/usr/bin/env python
# Lab 5

import os
import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


goal_status_updated = True
goal_subscribed = False
goal_status = 3


###################################
## Call Backs and Helper Functions
###################################

# Loads goal coordinates from the text file 
def get_checkpoints():

    global checkpoints, goal_subscribed

    with open(os.path.join(__location__, "global_waypoints.txt"), 'r') as infile:
        data = infile.readlines()

        number_of_points = len(data)

        checkpoints = np.empty((number_of_points,7))

        for i, waypoint in enumerate(data):
            checkpoints[i] = waypoint.split(',')
        
        goal_subscribed = True

    return checkpoints 


def goal_status_callback(goal_status_data):

    global goal_status, goal_status_updated
    
    goal_status = goal_status_data.status.status
    
    goal_status_updated = True


###################################
##  Main Function
###################################

def Init():

    global goal_status_updated

    goals = get_checkpoints()
    num_of_goals = goals.shape[0]
    flag = 0

    print(goals)
        
    rospy.init_node('waypoints_publisher', anonymous=True)

    # Publish the waypoints 
    waypoints_pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=10)

    # Subscribe to /odom
    rospy.Subscriber("/move_base/status", MoveBaseActionResult, goal_status_callback, queue_size=1)
    
    waypoints = PoseStamped()

    while not rospy.is_shutdown():
        
        if goal_status_updated == True and goal_subscribed == True:

            goal = goals[flag]
            print("\n Goal Coordinates: ", goal)

            if goal_status == 3:
                
                rospy.sleep(2)

                waypoints.header.frame_id = "map"
                waypoints.header.stamp = rospy.Time.now()
                waypoints.pose.position.x = goal[0]
                waypoints.pose.position.y = goal[1]
                waypoints.pose.position.z = goal[2]
                waypoints.pose.orientation.w = goal[3]
                waypoints.pose.orientation.x = goal[4]
                waypoints.pose.orientation.y = goal[5]
                waypoints.pose.orientation.z = goal[6]

                waypoints_pub.publish(waypoints)

                flag += 1
            
            else:
                
                print("Goal Status: ", goal_status)

            goal_status_updated = False

        else:
            
            if goal_subscribed == False:
                print("\n Goal not received")
            
            if goal_status_updated == False:
                print("\n Goal Status not updated")

    rospy.spin()


if __name__ == '__main__':
	try:
		Init()
	except rospy.ROSInterruptException:
		pass
