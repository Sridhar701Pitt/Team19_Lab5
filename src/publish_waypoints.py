# Lab 5

import os
import rospy
import numpy as np

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Loads goal coordinates from the text file 
def get_checkpoints():

    global checkpoints, goal_subscribed

    checkpoints = np.empty((3,7))

    with open(os.path.join(__location__, "global_waypoints.txt"), 'r') as infile:
        data = infile.readlines()
        for i, waypoint in enumerate(data):
            checkpoints[i] = waypoint.split(',')
        
        goal_subscribed = True

    #print("Checkpoints: ", checkpoints)

    return checkpoints 

###################################
##  Main Function
###################################

def Init():

    goals = get_checkpoints()

    print(goals)

    '''
        
    rospy.init_node('go_to_goal_DWA', anonymous=True)

    # Publish angle and distance
    velocity_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    # Visualise the best trajectory by publishing Marker message
    best_trajectory_pub = rospy.Publisher("best_trajectory", Marker, queue_size = 1)

    # Subscribe to LIDAR scan topic /scan
    rospy.Subscriber("/scan", LaserScan, scan_callback, queue_size=1)

    # Subscribe to /odom
    rospy.Subscriber("/odom", Odometry, odom_callback, queue_size=1)
    
    optimal_vel = Twist()

    while not rospy.is_shutdown():
        
        if scan_updated == True and goal_subscribed == True and odom_updated == True:
            dynamic_window = calc_dynamic_window(current_velocity)

            goal = goal[0]
            print("\n Goal Coordinates: ", goal[0], ",", goal[1])

            if linalg.norm(goal) > GOAL_THRESHOLD:
                obstacles_list = scan_to_obs()
                scan_updated = False
            
                best_trajectory = dwa_planning(dynamic_window, goal, obstacles_list)
                
                optimal_vel.linear.x = best_trajectory[0].velocity
                optimal_vel.angular.z = best_trajectory[0].yawrate

                visualise_trajectory(best_trajectory, 1, 0, 0, best_trajectory_pub)

            else:
                optimal_vel.linear.x = 0.0
                optimal_vel.angular.z = 0.0

            print("\n Optimal Velocity: ", optimal_vel.linear.x, "m/s", optimal_vel.angular.z, "rad/s")
            velocity_pub.publish(optimal_vel)

            odom_updated = False

        else:
            
            if scan_updated == False:
                print("\n Scan not updated")
            
            if goal_subscribed == False:
                print("\n Goal not received")
            
            if odom_updated == False:
                print("\n Odom not updated")

    rospy.spin()

    '''

if __name__ == '__main__':
	try:
		Init()
	except rospy.ROSInterruptException:
		pass