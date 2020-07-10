#!/usr/bin/env python
"""
@package odom_from_joint_transform
@file odom_from_joint_transform_impl.py
@author Norawit Nangsue
@brief Odometry-tf Generator from Joint Message used as a temporary module

Copyright (C) FIBO
FIBO
"""

import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
import tf

# protected region user include package begin #
from math import sin, cos, tan
from geometry_msgs.msg import Quaternion
# protected region user include package end #


class OdomFromJointTransformConfig(object):
    """
    set of static and dynamic parameters
    autogenerated: don't touch this class
    """
    def __init__(self):
        # parameters handled through the parameter server
        self.wheel_circ = 0.12566
        self.sep_dist = 0.20875
        self.front_cpr = 6144
        self.rear_cpr = 1440
        self.invert_mul = 1
        pass

    def __str__(self):
        msg = "Instance of OdomFromJointTransformConfig class: {"
        msg += "wheel_circ: {} ".format(self.wheel_circ)
        msg += "sep_dist: {} ".format(self.sep_dist)
        msg += "front_cpr: {} ".format(self.front_cpr)
        msg += "rear_cpr: {} ".format(self.rear_cpr)
        msg += "invert_mul: {} ".format(self.invert_mul)
        msg += "}"
        return msg


class OdomFromJointTransformData(object):
    """
    set of input / output handled through the update methods
    autogenerated: don't touch this class
    """
    def __init__(self):
        """
        Definition of the OdomFromJointTransformData attributes
        """
        # input data
        self.in_joint_state = JointState()
        self.in_joint_state_updated = bool()
        # output data
        self.out_odom = Odometry()
        self.out_odom_active = bool()
        pass

    def __str__(self):
        msg = "Instance of OdomFromJointTransformData class: \n {"
        msg += "in_joint_state: {} \n".format(self.in_joint_state)
        msg += "in_joint_state_updated: {} \n".format(self.in_joint_state_updated)
        msg += "out_odom: {} \n".format(self.out_odom_active)
        msg += "out_odom_active: {} \n".format(self.out_odom_active)
        msg += "}"
        return msg


class OdomFromJointTransformPassthrough(object):
    """
    set of passthrough elements slightly violating interface / implementation separation
    Autogenerated: don't touch this class
    """
    def __init__(self):
        """ Class to contain variable breaking the interface separation
        """
        self.odom_to_base_footprint = tf.TransformBroadcaster()
        pass


class OdomFromJointTransformImplementation(object):
    """
    Class to contain Developer implementation.
    """
    def __init__(self):
        """
        Definition and initialisation of class attributes
        """
        self.passthrough = OdomFromJointTransformPassthrough()

        # protected region user member variables begin #
        self.current_joint = [0, 0]
        self.joint_diff = 0
        # protected region user member variables end #

    def configure(self, config):
        """
        @brief configuration of the implementation
        @param      self The object
        @param      config set of configuration parameters
        @return True on success
        """
        # protected region user configure begin #
        rospy.loginfo('Odom from Joint Transform Started')
        return True
        # protected region user configure end #

    def update(self, data, config):
        """
        @brief { function_description }

        @param      self The object
        @param      data data handled through the ros class
        @param      config parameters handled through dyn. recon.

        @return nothing
        """
        # protected region user update begin #
        if data.in_joint_state_updated:
            if data.out_odom.header.seq == 0:
                self.current_joint = data.in_joint_state.position
                data.out_odom.header.seq = 1
                return
            self.joint_diff = data.in_joint_state.position[0] - self.current_joint[0]
            # Calculate Forward Kinematic
            dx_robot = config.invert_mul * config.wheel_circ * self.joint_diff / config.front_cpr
            da = dx_robot * - tan(data.in_joint_state.position[1] / config.rear_cpr * 2 * 3.14159) / config.sep_dist
            # Obtain time and relative time from last update
            time_cur = rospy.Time.now()
            time_rel = time_cur - data.out_odom.header.stamp
            # Define frame of reference
            data.out_odom.header.frame_id = 'odom'
            data.out_odom.child_frame_id = 'base_footprint'
            # Update Odom Pose
            data.out_odom.header.stamp = time_cur
            quat_past = (0, 0, data.out_odom.pose.pose.orientation.z, data.out_odom.pose.pose.orientation.w)
            yaw_past = tf.transformations.euler_from_quaternion(quat_past)[2]
            pos_cur = (data.out_odom.pose.pose.position.x + dx_robot * cos(yaw_past), 
                    data.out_odom.pose.pose.position.y + dx_robot * sin(yaw_past), 0)
            quat_cur = Quaternion(*tf.transformations.quaternion_from_euler(0, 0, yaw_past + da))
            data.out_odom.pose.pose.position.x = pos_cur[0]
            data.out_odom.pose.pose.position.y = pos_cur[1]
            data.out_odom.pose.pose.orientation = quat_cur
            # Update Odom Twist
            data.out_odom.twist.twist.linear.x = dx_robot / time_rel.to_sec()
            data.out_odom.twist.twist.angular.z = da / time_rel.to_sec()
            # tf
            self.passthrough.odom_to_base_footprint.sendTransform(pos_cur, (0, 0, quat_cur.z, quat_cur.w), time_cur, "base_footprint", "odom")
            
            #Update Current Pose
            self.current_joint = data.in_joint_state.position
        # protected region user update end #

    def terminate(self):
        """
        A function performed when Keyboard Interrupt trigger
	    This gives you a chance to save important data or clean clean object if needed
        """
        # protected region user terminate begin #
        pass
        # protected region user terminate end #


    # protected region user additional functions begin #
    # protected region user additional functions end #
