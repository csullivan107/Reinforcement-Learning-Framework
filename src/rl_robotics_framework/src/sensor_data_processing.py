#!/usr/bin/env python

'''
This script runs acts as the middleware for the state of the robot based on sensor readings. in the 
launch file for learning, the limits of the actuator operation determined from the calibration
cycle are set. This script maps the raw sensor readings in the actuartors to the 0-100% actuation
format that is expected by the RL algorithm. 

Author: Charles (Chuck) Sullivan
Last update: 9-13-2020
'''

import rospy
from std_msgs.msg import String
from rosserial_arduino.msg import Adc
from rl_robotics_framework.msg import sensor_processing

#these vvalues are ready for setting parameters in ROS
#ADC values taht are the limits of actuation
X_HIGH_RAW = rospy.get_param('/xSensorMax')
X_LOW_RAW = rospy.get_param('/xSensorMin')
Y_HIGH_RAW = rospy.get_param('/ySensorMax')
Y_LOW_RAW = rospy.get_param('/ySensorMin')

print ("XHigh: {}\tXMin: {}\tYMin: {}",format(X_HIGH_RAW),format(X_LOW_RAW) ,format(Y_LOW_RAW))

#define publisher
#message format - "x: num y: num"
pub = rospy.Publisher('robot_state', sensor_processing, queue_size = 30)

#this function maps the raw data from 0-1024  values to 0 - 100% actuation
#input is raw reading, what reading corresopnds to 0, and 100% actuation respectively
#adapted from arduino map function
def raw2rl_mapping(raw,zero_value,hundred_value):
    percentage = float((raw-zero_value)/(hundred_value-zero_value)*100)
    # print ("input: {}\tpercentage: {}",format(raw) ,format(percentage))

    #the machine learning script is expecting values from 0-100 - clip this data so that script doesnt fail
    if percentage > 100:
        percentage = 100.
    elif percentage < 0:
        percentage = 0.
   
    return percentage


def callback0(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", str(data.adc0))
    global X_LOW_RAW, X_HIGH_RAW, Y_HIGH_RAW, Y_LOW_RAW
    #Read in sensor data from Arduino
    x_sensor_reading = float(data.adc0)
    y_sensor_reading = float(data.adc1)
    #map readings from 0-1024 to percentages (see: calibration)
    x_mapped = raw2rl_mapping(x_sensor_reading,X_LOW_RAW,X_HIGH_RAW)
    y_mapped = raw2rl_mapping(y_sensor_reading,Y_LOW_RAW,Y_HIGH_RAW)
    #package message and publish
    message = sensor_processing()
    message.xSensor = x_mapped
    message.ySensor = y_mapped
    print(message)
    pub.publish(message)
    
    
def sensorProcessingNode():

    rospy.init_node('sensor_data_processing', anonymous=True)

    rospy.Subscriber("sensor_data", Adc, callback0)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':
    sensorProcessingNode()