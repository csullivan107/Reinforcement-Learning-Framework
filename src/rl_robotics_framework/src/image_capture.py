#!/usr/bin/env python3

'''
This script pulls an image from the webcam from the ground truth system. Every n seconds an image is
captured and published to the topic /bag_image. This is used in rosbag logging for the learning runs.


Author: Charles (Chuck) Sullivan
Last update: 9-13-2020
'''

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError

capture_rate = 15 #seconds

pub = rospy.Publisher('bag_image', Image, queue_size = 30)

def callback0(data):
	global capture_rate
	pub.publish(data)
	
	print("data published")

	rospy.sleep(capture_rate) #get an image every 'capture_rate' seconds

def imageCaptureNode():
	
	
	rospy.init_node('image_capture', anonymous=True)
	rospy.Subscriber("/usb_cam/image_raw", Image, callback0)
	    
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()


if __name__ == '__main__':
    imageCaptureNode()
