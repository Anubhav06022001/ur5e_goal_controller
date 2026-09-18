import math
import rclpy
from rclpy.node import Node
from moveit_msgs.srv import GetPositionIK
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

JOINT_NAMES = ['shoulder_pan_joint','shoulder_lift_joint','elbow_joint','wrist_1_joint','wrist_2_joint','wrist_3_joint']


def rpy_to_quaternion(roll, pitch, yaw):
    cr, sr = math.cos(roll/2), math.sin(roll/2)
    cp, sp = math.cos(pitch/2), math.sin(pitch/2)
    cy, sy = math.cos(yaw/2), math.sin(yaw/2)
    return (sr*cp*cy-cr*sp*sy, cr*sp*cy+sr*cp*sy, cr*cp*sy-sr*sp*cy, cr*cp*cy+sr*sp*sy)


class UR5eController(Node):
    def __init__(self):
        super().__init__('ur5e_goal_controller')

        self.ik_client = self.create_client(GetPositionIK, '/compute_ik')
        self.publisher = self.create_publisher(
            JointTrajectory,
            '/scaled_joint_trajectory_controller/joint_trajectory',10)

        self.get_logger().info('Waiting for MoveIt IK service...')
        self.ik_client.wait_for_service()

        try:
            x, y, z = map(float, input('Enter target position (x y z) in meters: ').split())
            roll, pitch, yaw = map(float, input('Enter target orientation (roll pitch yaw) in radians: ').split())
        except ValueError:
            self.get_logger().error('Invalid input. Please enter exactly 3 numbers for each.')
            return

        qx, qy, qz, qw = rpy_to_quaternion(roll, pitch, yaw)

        req = GetPositionIK.Request()
        req.ik_request.group_name = 'ur_manipulator'
        req.ik_request.pose_stamped.header.frame_id = 'base'

        req.ik_request.pose_stamped.pose.position.x = x
        req.ik_request.pose_stamped.pose.position.y = y
        req.ik_request.pose_stamped.pose.position.z = z

        req.ik_request.pose_stamped.pose.orientation.x = qx
        req.ik_request.pose_stamped.pose.orientation.y = qy
        req.ik_request.pose_stamped.pose.orientation.z = qz
        req.ik_request.pose_stamped.pose.orientation.w = qw

        future = self.ik_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        response = future.result()

        if response is None or response.error_code.val != 1:
            self.get_logger().error(
                'No valid IK solution found. Try a different reachable pose.'
            )
            return

        joint_state = response.solution.joint_state
        q = [joint_state.position[joint_state.name.index(name)] for name in JOINT_NAMES]

        self.get_logger().info(f'IK solution: {q}')

        msg = JointTrajectory()
        msg.joint_names = JOINT_NAMES

        point = JointTrajectoryPoint()
        point.positions = q
        point.time_from_start.sec = 5
        msg.points.append(point)

        self.publisher.publish(msg)
        self.get_logger().info('Trajectory sent to UR5e.')


def main():
    rclpy.init()
    node = UR5eController()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()