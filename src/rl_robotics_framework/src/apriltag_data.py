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
x_calib_zero = 0
y_calib_zero = 0

# def calculateVector(xP,yP,zP,xO,yO,zO,wO):


#define publisher
#message format - "x: num y: num"
pub = rospy.Publisher('/gnd_pos_truth', apriltag_data, queue_size = 30)


def callback0(data):

    len = .020 #20 mm in meter representation

    x_pos = data.detections[0].pose.pose.pose.position.x
    y_pos = data.detections[0].pose.pose.pose.position.y
    z_pos = data.detections[0].pose.pose.pose.position.z
    #quaternian orientation
    x_quat = data.detections[0].pose.pose.pose.orientation.x
    y_quat = data.detections[0].pose.pose.pose.orientation.y
    z_quat = data.detections[0].pose.pose.pose.orientation.z
    w_quat = data.detections[0].pose.pose.pose.orientation.w

    # tag_quat = np.quaternian(w_quat,x_quat,y_quat,z_quat)
    # rot_mat = np.quaternian.as_rotation_matrix(tag_quat)
    

    tag_size = data.detections[0].size
    tag_id = data.detections[0].id
    message = apriltag_data()
    message.x_pos_gnd = x_pos
    message.y_pos_gnd = y_pos

    
    
    pub.publish(message)


def apriltagProcessing():
    rospy.init_node('apriltag_data_processing', anonymous=True)

    rospy.Subscriber("/tag_detections", AprilTagDetectionArray, callback0)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    apriltagProcessing()