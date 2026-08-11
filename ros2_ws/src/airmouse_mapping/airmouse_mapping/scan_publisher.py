import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class ScanPublisher(Node):

    def __init__(self):
        super().__init__('scan_publisher')

        self.publisher = self.create_publisher(
            LaserScan,
            '/scan',
            10
        )

        self.timer = self.create_timer(0.1, self.publish_scan)

    def ray_distance(self, angle):
        # Room boundaries: x = +/-5 m, y = +/-4 m
        dx = math.cos(angle)
        dy = math.sin(angle)

        distances = []

        if abs(dx) > 1e-9:
            for wall_x in (-5.0, 5.0):
                t = wall_x / dx
                if t > 0:
                    y = t * dy
                    if -4.0 <= y <= 4.0:
                        distances.append(t)

        if abs(dy) > 1e-9:
            for wall_y in (-4.0, 4.0):
                t = wall_y / dy
                if t > 0:
                    x = t * dx
                    if -5.0 <= x <= 5.0:
                        distances.append(t)

        # Simple internal obstacle: square pillar
        obstacle_x = 2.0
        obstacle_y = 1.0
        half_size = 0.6

        # Ray-box intersection
        if abs(dx) > 1e-9:
            for x in (obstacle_x - half_size, obstacle_x + half_size):
                t = (x) / dx
                if t > 0:
                    y = t * dy
                    if obstacle_y - half_size <= y <= obstacle_y + half_size:
                        distances.append(t)

        if abs(dy) > 1e-9:
            for y in (obstacle_y - half_size, obstacle_y + half_size):
                t = y / dy
                if t > 0:
                    x = t * dx
                    if obstacle_x - half_size <= x <= obstacle_x + half_size:
                        distances.append(t)

        if distances:
            return min(distances)

        return 10.0

    def publish_scan(self):
        scan = LaserScan()

        scan.header.stamp = self.get_clock().now().to_msg()
        scan.header.frame_id = 'laser'

        scan.angle_min = -math.pi
        scan.angle_max = math.pi
        scan.angle_increment = math.radians(1.0)

        scan.range_min = 0.05
        scan.range_max = 10.0

        scan.ranges = [
            min(self.ray_distance(angle), 10.0)
            for angle in (
                -math.pi + i * math.radians(1.0)
                for i in range(360)
            )
        ]

        self.publisher.publish(scan)


def main(args=None):
    rclpy.init(args=args)

    node = ScanPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
