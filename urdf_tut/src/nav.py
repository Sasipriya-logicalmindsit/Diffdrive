#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def send_goal(x, y, w):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = w

    client.send_goal(goal)
    client.wait_for_result()

    return client.get_result()

def main():
    rospy.init_node('nav')

    global client
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goals = [
        (1.0, 2.0, 1.0),
        (2.5, 3.5, 1.0),
        (8.0, -2.0, 1.0),
        (7.0, 3.0, 1.0)
        

    ]

    wait_time = 3 

    for i, goal in enumerate(goals):
        rospy.loginfo(f"Sending goal {i+1}: {goal}")
        result = send_goal(goal[0], goal[1], goal[2])

        if result:
            rospy.loginfo(f"Reached goal {i+1}: {goal}")
            rospy.loginfo(f"Waiting for {wait_time} seconds...")
            rospy.sleep(wait_time)
        else:
            rospy.logwarn(f"Failed to reach goal {i+1}: {goal}")
            return

    rospy.loginfo("Goals reached successfully!")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass