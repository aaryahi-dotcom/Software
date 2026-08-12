import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MissionManager(Node):

    def __init__(self):
        super().__init__('mission_manager')

        self.state = 'IDLE'
        self.survivor_count = 0

        self.status_publisher = self.create_publisher(
            String,
            '/mission_status',
            10
        )

        self.survivor_subscriber = self.create_subscription(
            String,
            '/survivor_detected',
            self.survivor_callback,
            10
        )

        self.return_subscriber = self.create_subscription(
            String,
            '/return_to_entry',
            self.return_callback,
            10
        )

        self.complete_subscriber = self.create_subscription(
            String,
            '/mission_complete',
            self.complete_callback,
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_status
        )

        self.get_logger().info('Mission Manager started')

        self.start_mission()

    def publish_status(self):
        message = String()

        message.data = (
            f'STATE={self.state}, '
            f'SURVIVORS={self.survivor_count}'
        )

        self.status_publisher.publish(message)

    def start_mission(self):
        self.state = 'EXPLORING'
        self.get_logger().info('Mission State: EXPLORING')

    def survivor_callback(self, message):
        if self.state == 'EXPLORING':
            self.survivor_count += 1
            self.state = 'SURVIVOR_FOUND'

            self.get_logger().info(
                f'Survivor detected! Total survivors: '
                f'{self.survivor_count}'
            )

    def return_callback(self, message):
        if self.state in ['EXPLORING', 'SURVIVOR_FOUND']:
            self.state = 'RETURNING'
            self.get_logger().info(
                'Mission State: RETURNING'
            )

    def complete_callback(self, message):
        if self.state == 'RETURNING':
            self.state = 'COMPLETE'
            self.get_logger().info(
                'Mission State: COMPLETE'
            )


def main(args=None):
    rclpy.init(args=args)

    node = MissionManager()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
