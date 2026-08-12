import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String


class ReturnToEntry(Node):

    def __init__(self):
        super().__init__('return_to_entry')

        self.entry_pose = None

        self.pose_subscription = self.create_subscription(
            PoseStamped,
            '/robot_pose',
            self.pose_callback,
            10
        )

        self.return_subscription = self.create_subscription(
            String,
            '/return_command',
            self.return_callback,
            10
        )

        self.return_publisher = self.create_publisher(
            PoseStamped,
            '/return_to_entry',
            10
        )

        self.get_logger().info('Return-to-Entry started')
        self.get_logger().info('Waiting for robot pose...')

    def pose_callback(self, msg):

        if self.entry_pose is None:
            self.entry_pose = msg

            self.get_logger().info(
                f'Entry position saved: '
                f'({msg.pose.position.x:.2f}, '
                f'{msg.pose.position.y:.2f})'
            )

    def return_callback(self, msg):

        if msg.data.upper() != 'RETURN':
            return

        if self.entry_pose is None:
            self.get_logger().warning(
                'Cannot return: entry position not available'
            )
            return

        target = PoseStamped()

        target.header = self.entry_pose.header
        target.header.frame_id = 'map'
        target.pose = self.entry_pose.pose

        self.return_publisher.publish(target)

        self.get_logger().info(
            f'Return target published: '
            f'({target.pose.position.x:.2f}, '
            f'{target.pose.position.y:.2f})'
        )


def main(args=None):

    rclpy.init(args=args)

    node = ReturnToEntry()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
