import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class RobotMotion(Node):

    def __init__(self):
        super().__init__('robot_motion')

        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.publish_tf)
        self.start_time = self.get_clock().now()

    def publish_tf(self):
        elapsed = (
            self.get_clock().now() - self.start_time
        ).nanoseconds / 1e9

        t = elapsed % 40.0

        if t < 10.0:
            x = -3.0 + 0.6 * t
            y = -2.0
        elif t < 20.0:
            x = 3.0
            y = -2.0 + 0.4 * (t - 10.0)
        elif t < 30.0:
            x = 3.0 - 0.6 * (t - 20.0)
            y = 2.0
        else:
            x = -3.0
            y = 2.0 - 0.4 * (t - 30.0)

        msg = TransformStamped()

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'odom'
        msg.child_frame_id = 'base_footprint'

        msg.transform.translation.x = x
        msg.transform.translation.y = y
        msg.transform.translation.z = 0.0

        msg.transform.rotation.x = 0.0
        msg.transform.rotation.y = 0.0
        msg.transform.rotation.z = 0.0
        msg.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(msg)


def main(args=None):
    rclpy.init(args=args)
    node = RobotMotion()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
