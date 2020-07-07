#!/usr/bin/env python
"""
@package ackermann_twist_joy
@file teleop_node_ros.py
@author Norawit Nangsue
@brief Convert Input Axes from JoyMessage into Ackermann Drive Message

Copyright (C) FIBO
MIT
"""

from copy import deepcopy
import rospy

# ROS message & services includes
from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import Joy

# other includes
from ackermann_twist_joy import teleop_node_impl


class TeleopNodeROS(object):
    """
    ROS interface class, handling all communication with ROS
    """
    def __init__(self):
        """
        Attributes definition
        """
        self.component_data_ = teleop_node_impl.TeleopNodeData()
        self.component_config_ = teleop_node_impl.TeleopNodeConfig()
        self.component_implementation_ = teleop_node_impl.TeleopNodeImplementation()

        # handling parameters from the parameter server
        self.component_config_.enb_index = rospy.get_param("~enb_index", 5)
        self.component_config_.linear_index = rospy.get_param("~linear_index", 4)
        self.component_config_.steering_index = rospy.get_param("~steering_index", 0)
        self.component_config_.linear_vel_scale = rospy.get_param("~linear_vel_scale", 0.2)
        self.component_config_.steering_pos_scale = rospy.get_param("~steering_pos_scale", 0.7853975)
        # handling publishers
        self.ackermann_cmd_ = rospy.Publisher('ackermann_cmd', AckermannDriveStamped, queue_size=1)
        # handling subscribers
        self.joy_ = rospy.Subscriber('joy', Joy, self.topic_callback_joy)

    def topic_callback_joy(self, msg):
        """
        callback called at message reception
        """
        self.component_data_.in_joy = msg
        self.component_data_.in_joy_updated = True

    def configure(self):
        """
        function setting the initial configuration of the node
        """
        return self.component_implementation_.configure(self.component_config_)

    def activate_all_output(self):
        """
        activate all defined output
        """
        self.component_data_.out_ackermann_cmd_active = True
        pass

    def set_all_input_read(self):
        """
        set related flag to state that input has been read
        """
        self.component_data_.in_joy_updated = False
        pass

    def update(self, event):
        """
        @brief update function

        @param      self The object
        @param      event The event

        @return { description_of_the_return_value }
        """
        self.activate_all_output()
        config = deepcopy(self.component_config_)
        data = deepcopy(self.component_data_)
        self.set_all_input_read()
        self.component_implementation_.update(data, config)

        try:
            self.component_data_.out_ackermann_cmd_active = data.out_ackermann_cmd_active
            self.component_data_.out_ackermann_cmd = data.out_ackermann_cmd
            if self.component_data_.out_ackermann_cmd_active:
                self.ackermann_cmd_.publish(self.component_data_.out_ackermann_cmd)
        except rospy.ROSException as error:
            rospy.logerr("Exception: {}".format(error))


def main():
    """
    @brief Entry point of the package.
    Instanciate the node interface containing the Developer implementation
    @return nothing
    """
    rospy.init_node("teleop_node", anonymous=False)

    node = TeleopNodeROS()
    if not node.configure():
        rospy.logfatal("Could not configure the node")
        rospy.logfatal("Please check configuration parameters")
        rospy.logfatal("{}".format(node.component_config_))
        return

    rospy.Timer(rospy.Duration(1.0 / 20), node.update)
    rospy.spin()
    node.component_implementation_.terminate()
