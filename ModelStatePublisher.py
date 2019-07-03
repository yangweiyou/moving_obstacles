#!/usr/bin/env python
import roslib; roslib.load_manifest('gazebo_ros')
import sys
from gazebo_msgs.msg import ModelState
import rospy
from std_srvs.srv import Empty
from gazebo_msgs.srv import GetModelState

print("Imports successful")

def main():
	pub = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=10)
	rospy.init_node('moving_obstacles')
	rate = rospy.Rate(10)	
	print('ROS initializing, node creation, rate setting done')

	g_get_state = rospy.ServiceProxy("/gazebo/get_model_state", GetModelState)
	print("line 1 ok")
	rospy.wait_for_service("/gazebo/get_model_state")
	print("line 2 ok")
	init_state = g_get_state(model_name="unit_sphere")
	print("line 3 ok")

	state=ModelState()
	print("state object created")
	state.model_name = "unit_sphere"
	print("state model name ok")
	state.pose.position.x=init_state.pose.position.x
	state.pose.position.y=init_state.pose.position.y
	print('positions initialized')

	while not rospy.is_shutdown():
		i=0
		first_loop_indicator = 0
		for j in range(60):
			state.pose.position.x=state.pose.position.x+i
		
			pub.publish(state)

			i=i+0.001
			rate.sleep()
			print("Yes")
			first_loop_indicator += 1
		print("first_loop_indicator is " + str(first_loop_indicator))
		i=0
		second_loop_indicator=0	
		for j in range(60):
			state.pose.position.x=state.pose.position.x-i
		
			pub.publish(state)

			i=i+0.001
			rate.sleep()	
			second_loop_indicator += 1
		print("second_loop_indicator is" + str(second_loop_indicator))

if __name__ == '__main__':
	try:
		print('Going to begin main method')
		main()

	except rospy.ROSInterruptException:

		pass	
