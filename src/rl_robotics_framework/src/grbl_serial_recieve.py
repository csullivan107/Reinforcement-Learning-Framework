#!/usr/bin/env python

'''
This script acts a means to recieve grbl CNC commands from the grbl controller via serial port.
It publishes this data to the topic /grbl_feedback.

This data is not used in the final version in which learning takes place. It is very useful for
debugging and setup.

Author: Charles (Chuck) Sullivan
Last update: 9-13-2020
'''


import rospy,serial,time, sys
from std_msgs.msg import String


print(sys.version)


usbPort = rospy.get_param('/grbl_arduino') #get global parameter

grblArduino = serial.Serial(usbPort, 115200, timeout=.1, exclusive=0)

print("serial information: ")
print("\t" + grblArduino.name)

def grbl_listener():

	pub = rospy.Publisher('grbl_feedback', String, queue_size=100)
	rospy.init_node('grbl_serial_recieve', anonymous=True)
	rate = rospy.Rate(4) # 1hz
	grblMsg = ""
	
	while not rospy.is_shutdown():
		if grblArduino.inWaiting():

			grblMsg = grblArduino.read(grblArduino.inWaiting())

		else:
			grblMsg = "nothing from grbl controller"
		
		rospy.loginfo(grblMsg)
		pub.publish(grblMsg)

		grblMsg = ""
		rate.sleep()


        

if __name__ == '__main__':
    grbl_listener()

