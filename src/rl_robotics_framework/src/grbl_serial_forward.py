#!/usr/bin/env python

'''
This script acts a means to forward grbl CNC commands to the grbl controller via serial port.

M8 and M9 are added to the g-code string to turn on and off the coolant pin respectively. this 
is used to determine if an action is complete by the system monitoring section of the framework.

Author: Charles (Chuck) Sullivan
Last update: 9-13-2020
'''

import rospy,serial,time, sys
from std_msgs.msg import String


print(sys.version)
usbPort = rospy.get_param('/grbl_arduino') #get global parameter

#get usb port from arguments

#grblArduino = serial.Serial('/dev/ttyACM2', 115200, timeout=.1, exclusive=0)
grblArduino = serial.Serial(usbPort, 115200, timeout=.1, exclusive=0)

print("serial information: ")
print("\t" + grblArduino.name)

#call back is called anytime the subscriber gets data from the topic
def callback(data):
    #str2send = String()
    str2send = "M8" + '\n' + data.data + '\n' + "M9" + '\n'
    rospy.loginfo(rospy.get_caller_id() + "I heard '%s' and am sending '%s'", data.data, str2send)
    
    grblArduino.write(str2send)
    
def grbl_forward():

    
    rospy.init_node('grbl_serial_forward', anonymous=True)

    rospy.Subscriber("grbl_commands", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    grbl_forward()
