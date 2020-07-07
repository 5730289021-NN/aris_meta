# ackermann_twist_joy

## General description of the package

<!--- protected region package description begin -->
Convert Input Axes from JoyMessage into Ackermann Drive Message
<!--- protected region package description end -->

<!--- todo How to handle the image generation -->
<!--- <img src="./model/teleop_node.png" width="300px" />-->

## Node: teleop_node

Update frequency: 20 Hz.

<!--- protected region teleop_node begin -->
<!--- protected region teleop_node end -->

### Static Parameters

All static parameters can be set through the command line:

```shell
rosrun ackermann_twist_joy teleop_node [param_name]:=[new_value]
```

`enb_index` *(int, default: 5)*
<!--- protected region param enb_index begin -->
Enable Button Index
<!--- protected region param enb_index end -->
`linear_index` *(int, default: 4)*
<!--- protected region param linear_index begin -->
Linear Drive Joy-axis Index
<!--- protected region param linear_index end -->
`steering_index` *(int, default: 0)*
<!--- protected region param steering_index begin -->
Steering Joy-axis Index
<!--- protected region param steering_index end -->
`linear_vel_scale` *(double, default: 0.2)*
<!--- protected region param linear_vel_scale begin -->
Robot Linear Velocity Scale
<!--- protected region param linear_vel_scale end -->
`steering_pos_scale` *(double, default: 0.7853975)*
<!--- protected region param steering_pos_scale begin -->
Robot Steering Position Scale
<!--- protected region param steering_pos_scale end -->

### Published Topics

A topic can be remapped from the command line:

```shell
rosrun ackermann_twist_joy teleop_node [old_name]:=[new_name]
```

`ackermann_cmd` *(ackermann_msgs::AckermannDriveStamped)*
<!--- protected region publisher ackermann_cmd begin -->
Ackermann Drive Stamped
<!--- protected region publisher ackermann_cmd end -->

### Subscribed Topics

A topic can be remapped from the command line:

```shell
rosrun ackermann_twist_joy teleop_node [old_name]:=[new_name]
```

`joy` *(sensor_msgs::Joy)*
<!--- protected region subscriber joy begin -->
Input Joy
<!--- protected region subscriber joy end -->

---

*Package generated with the [ROS Package Generator](https://github.com/tecnalia-advancedmanufacturing-robotics/ros_pkg_gen).*
# ackermann_twist_joy
