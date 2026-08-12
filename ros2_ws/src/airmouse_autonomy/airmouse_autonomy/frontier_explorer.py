import math

import rclpy
from rclpy.node import Node

from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped


class FrontierExplorer(Node):

    def __init__(self):
        super().__init__('frontier_explorer')

        self.map_subscription = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.map_callback,
            10
        )

        self.target_publisher = self.create_publisher(
            PoseStamped,
            '/exploration_target',
            10
        )

        self.last_target = None

        self.get_logger().info('Frontier Explorer started')
        self.get_logger().info('Waiting for /map...')

    def map_callback(self, map_msg):

        width = map_msg.info.width
        height = map_msg.info.height
        resolution = map_msg.info.resolution
        origin = map_msg.info.origin

        expected_size = width * height

        if len(map_msg.data) < expected_size:
            self.get_logger().warning(
                f'Invalid map: expected {expected_size} cells, '
                f'received {len(map_msg.data)}'
            )
            return

        frontiers = self.find_frontiers(
            map_msg.data,
            width,
            height
        )

        if not frontiers:
            self.get_logger().info(
                'No frontier found. Exploration may be complete.'
            )
            return

        target_x, target_y, score, size = self.select_frontier(
            frontiers,
            width,
            height
        )

        world_x = (
            origin.position.x +
            (target_x + 0.5) * resolution
        )

        world_y = (
            origin.position.y +
            (target_y + 0.5) * resolution
        )

        target_key = (
            round(world_x, 2),
            round(world_y, 2)
        )

        if target_key == self.last_target:
            return

        self.last_target = target_key

        target = PoseStamped()

        target.header = map_msg.header
        target.header.frame_id = 'map'

        target.pose.position.x = world_x
        target.pose.position.y = world_y
        target.pose.position.z = 0.0

        target.pose.orientation.w = 1.0

        self.target_publisher.publish(target)

        self.get_logger().info(
            f'New frontier target: '
            f'({world_x:.2f}, {world_y:.2f}) '
            f'| size={size} '
            f'| score={score:.2f}'
        )

    def find_frontiers(self, data, width, height):

        frontier_cells = []

        for y in range(1, height - 1):
            for x in range(1, width - 1):

                index = y * width + x

                if data[index] != 0:
                    continue

                neighbors = [
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1)
                ]

                for nx, ny in neighbors:

                    neighbor_index = ny * width + nx

                    if data[neighbor_index] == -1:
                        frontier_cells.append((x, y))
                        break

        return frontier_cells

    def select_frontier(
        self,
        frontier_cells,
        width,
        height
    ):

        center_x = width / 2.0
        center_y = height / 2.0

        best_cell = frontier_cells[0]
        best_score = float('-inf')
        best_size = 1

        for cell_x, cell_y in frontier_cells:

            nearby_count = 0

            for other_x, other_y in frontier_cells:

                distance = math.sqrt(
                    (cell_x - other_x) ** 2 +
                    (cell_y - other_y) ** 2
                )

                if distance <= 2.0:
                    nearby_count += 1

            distance_from_center = math.sqrt(
                (cell_x - center_x) ** 2 +
                (cell_y - center_y) ** 2
            )

            score = (
                nearby_count * 2.0
                - distance_from_center
            )

            if score > best_score:
                best_score = score
                best_cell = (cell_x, cell_y)
                best_size = nearby_count

        return (
            best_cell[0],
            best_cell[1],
            best_score,
            best_size
        )


def main(args=None):

    rclpy.init(args=args)

    node = FrontierExplorer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
