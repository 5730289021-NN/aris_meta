#!/usr/bin/env python
"""
@package odom_from_joint_transform
@file odom_from_joint_transform_ros.py
@author Norawit Nangsue
@brief Odometry-tf Generator from Joint Message used as a temporary module

Copyright (C) FIBO
FIBO
"""

from copy import deepcopy
import rospy

# ROS message & services includes
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState

# other includes
from odom_from_joint_transform import odom_from_joint_transform_impl


class OdomFromJointTransformROS(object):
    """
    ROS interface class, handling all communication with ROS
    """
    def __init__(self):
        """
        Attributes definition
        """
        self.component_data_ = odom_from_joint_transform_impl.OdomFromJointTransformData()
        self.component_config_ = odom_from_joint_transform_impl.OdomFromJointTransformConfig()
        self.component_implementation_ = odom_from_joint_transform_impl.OdomFromJointTransformImplementation()

        # handling parameters from the parameter server
        self.component_config_.wheel_circ = rospy.get_param("~wheel_circ", 0.12566)
        self.component_config_.sep_dist = rospy.get_param("~sep_dist", 0.20875)
        self.component_config_.front_cpr = rospy.get_param("~front_cpr", 6144)
        self.component_config_.rear_cpr = rospy.get_param("~rear_cpr", 1440)
        self.component_config_.invert_mul = rospy.get_param("~invert_mul", 1)
        # handling publishers
        self.odom_ = rospy.Publisher('odom', Odometry, queue_size=1)
        # handling subscribers
        self.joint_state_ = rospy.Subscriber('joint_state', JointState, self.topic_callback_joint_state)

    def topic_callback_joint_state(self, msg):
        """
        callback called at message reception
        """
        self.component_data_.in_joint_state = msg
        self.component_data_.in_joint_state_updated = True

    def configure(self):
        """
        function setting the initial configuration of the node
        """
        return self.component_implementation_.configure(self.component_config_)

    def activate_all_output(self):
        """
        activate all defined output
        """
        self.component_data_.out_odom_active = True
        pass

    def set_all_input_read(self):
        """
        set related flag to state that input has been read
        """
        self.component_data_.in_joint_state_updated = False
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
            self.component_data_.out_odom_active = data.out_odom_active
            self.component_data_.out_odom = data.out_odom
            if self.component_data_.out_odom_active:
                self.odom_.publish(self.component_data_.out_odom)
        except rospy.ROSException as error:
            rospy.logerr("Exception: {}".format(error))


def main():
    """
    @brief Entry point of the package.
    Instanciate the node interface containing the Developer implementation
    @return nothing
    """
    rospy.init_node("odom_from_joint_transform", anonymous=False)

    node = OdomFromJointTransformROS()
    if not node.configure():
        rospy.logfatal("Could not configure the node")
        rospy.logfatal("Please check configuration parameters")
        rospy.logfatal("{}".format(node.component_config_))
        return

    rospy.Timer(rospy.Duration(1.0 / 20), node.update)
    rospy.spin()
    node.component_implementation_.terminate()
