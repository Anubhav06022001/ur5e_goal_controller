# 🤖 UR5e Goal Controller

ROS 2 package for commanding the **UR5e end effector** to a user-specified position and orientation using **MoveIt inverse kinematics**.

---

## 🚀 Overview

The node accepts a target end-effector pose from the terminal, requests an inverse-kinematics solution from **MoveIt**, and sends the resulting joint positions to the **UR5e trajectory controller**.

---

## 🔄 Pipeline

```text
┌──────────────┐
│  User Input  │
└──────┬───────┘
       ↓
┌─────────────────────┐
│ RPY → Quaternion    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│     MoveIt IK       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   Joint Positions   │
└──────────┬──────────┘
           ↓
┌──────────────────────────────┐
│ Scaled Joint Trajectory      │
│ Controller                   │
└──────────┬───────────────────┘
           ↓
      ┌──────────┐
      │   UR5e   │
      └────┬─────┘
           ↓
      ┌──────────┐
      │   RViz   │
      └──────────┘
```

## 🧰 Requirements

- Ubuntu 22.04
- ROS 2 Humble
- Universal Robots ROS 2 Driver
- MoveIt 2
- UR5e

> **Note:** The implementation uses **fake hardware**, so no physical UR5e is required.

## 📦 Package Structure

```text
ur5e_goal_controller/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
├── test/
└── ur5e_goal_controller/
    ├── __init__.py
    └── move_ur5e.py
```

## ▶️ Running the Simulation

### 1. Start the UR5e Driver

Open a terminal and run:

```bash
source /opt/ros/humble/setup.bash
ros2 launch ur_robot_driver ur_control.launch.py \
  ur_type:=ur5e \
  robot_ip:=0.0.0.0 \
  use_fake_hardware:=true \
  launch_rviz:=true
```

### 2. Start MoveIt

Open a second terminal:

```bash
source /opt/ros/humble/setup.bash
ros2 launch ur_moveit_config ur_moveit.launch.py \
  ur_type:=ur5e \
  launch_rviz:=false
```

### 3. Build and Source the Package

Open a third terminal:

```bash
source /opt/ros/humble/setup.bash
cd ~/Documents/mowito/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

### 4. Run the Controller

```bash
ros2 run ur5e_goal_controller move_ur5e
```

Enter the target position and orientation:

```
Enter target position (x y z) in meters: 0.30 0.40 0.20
Enter target orientation (roll pitch yaw) in radians: 0 0 0
```

---

## ⚙️ Implementation

The controller follows this pipeline:

1. Read the target Cartesian position and orientation from the terminal.
2. Convert roll-pitch-yaw (RPY) to a quaternion.
3. Send the target pose to MoveIt's `/compute_ik` service.
4. Extract the six UR5e joint positions from the IK solution.
5. Create a `JointTrajectory` message.
6. Publish the trajectory to the `scaled_joint_trajectory_controller`.
7. The UR5e moves to the target configuration and the motion is visualized in RViz.

---


## 👤 Author

**Anubhav Tripathi**