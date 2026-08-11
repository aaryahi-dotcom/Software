"""Launch the perception detector node with config."""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory("airmouse_perception")
    params_file = os.path.join(pkg_share, "config", "perception_params.yaml")

    return LaunchDescription(
        [
            Node(
                package="airmouse_perception",
                executable="detector_node",
                name="detector_node",
                output="screen",
                parameters=[params_file],
            ),
        ]
    )