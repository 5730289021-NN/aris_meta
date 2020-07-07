# odom_from_joint_transform

## General description of the package

<!--- protected region package description begin -->
Odometry-tf Generator from Joint Message used as a temporary module
<!--- protected region package description end -->

<!--- todo How to handle the image generation -->
<!--- <img src="./model/odom_from_joint_transform.png" width="300px" />-->

## Node: odom_from_joint_transform

Update frequency: 20 Hz.

This node is using `\tf` to broadcast transforms.

<!--- protected region odom_from_joint_transform begin -->
<!--- protected region odom_from_joint_transform end -->

### Static Parameters

All static parameters can be set through the command line:

```shell
rosrun odom_from_joint_transform odom_from_joint_transform [param_name]:=[new_value]
```

`wheel_circ` *(double, default: 0.12566)*
<!--- protected region param wheel_circ begin -->
Circumstance of the wheel (2*PI*radius)
<!--- protected region param wheel_circ end -->
`sep_dist` *(double, default: 0.20875)*
<!--- protected region param sep_dist begin -->
Wheel Seperation Distance
<!--- protected region param sep_dist end -->
`front_cpr` *(int, default: 6144)*
<!--- protected region param front_cpr begin -->
Front Wheel Count to Meter Unit Ratio
<!--- protected region param front_cpr end -->
`rear_cpr` *(int, default: 1440)*
<!--- protected region param rear_cpr begin -->
Steering Angle Count to Radian Unit Ratio
<!--- protected region param rear_cpr end -->
`invert_mul` *(int, default: 1)*
<!--- protected region param invert_mul begin -->
Invert Multiplication
<!--- protected region param invert_mul end -->

### Published Topics

A topic can be remapped from the command line:

```shell
rosrun odom_from_joint_transform odom_from_joint_transform [old_name]:=[new_name]
```

`odom` *(nav_msgs::Odometry)*
<!--- protected region publisher odom begin -->
Wheel Odometry
<!--- protected region publisher odom end -->

### Subscribed Topics

A topic can be remapped from the command line:

```shell
rosrun odom_from_joint_transform odom_from_joint_transform [old_name]:=[new_name]
```

`joint_state` *(sensor_msgs::JointState)*
<!--- protected region subscriber joint_state begin -->
Robot Joint States
<!--- protected region subscriber joint_state end -->

---

*Package generated with the [ROS Package Generator](https://github.com/tecnalia-advancedmanufacturing-robotics/ros_pkg_gen).*
