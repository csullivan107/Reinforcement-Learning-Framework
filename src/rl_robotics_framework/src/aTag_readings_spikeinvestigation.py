#!/usr/bin/env python

'''
This script subscribes to apriltag algorithms /tag_detections topic. This is to be used as the
ground truth system for the rl_robotics_framework. It packages that data up for use in the RL
algorithm script using a custom message. The original implementation does not do much, just forwards
the data, but this should be used as an example for building middleware between ANY ground truth
system that you may have. 

-Note: There is some code involving the quaternion published by the apriltags algorithm. this was 
and attempt to get more info from the april tag. this was not fully explored during the initial 
thesis work, but is left in to help future work get tag orientation from the data. 

Author: Charles (Chuck) Sullivan
Last update: 9-13-2020
'''


import rospy
from std_msgs.msg import String
from apriltag_ros.msg import AprilTagDetectionArray
from rl_robotics_framework.msg import apriltag_data
import numpy as np
import quaternion



#these values will be used to 0 out each episode

y_calib_zero = 0




#define publisher


y_avg = []
count = 0
capture_rate = 1

def callback0(data):
	global capture_rate, y_avg,count
	print("data collected...")
	y_pos = data.detections[0].pose.pose.pose.position.y
	y_avg.append(y_pos)
	count = count+1

	rospy.sleep(capture_rate)

	if count == 10:
		avg = np.mean(y_avg)
		sdev = np.std(y_avg)
		print("Data Collected and processed")
		print("Average: " + str(avg))
		print("std dev: " + str(sdev))
		quit()
	
	



def ydata():
    rospy.init_node('ydata_collection', anonymous=True)

    rospy.Subscriber("/tag_detections", AprilTagDetectionArray, callback0)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
	print("Calculating avg Data...")
	ydata()