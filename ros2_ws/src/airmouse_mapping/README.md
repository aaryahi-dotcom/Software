# airmouse_mapping — Role 2: Mapping & SLAM

RPLIDAR → occupancy grid, TF tree, loop closure, corridor/room labelling. Uses
`slam_toolbox`; simulated LiDAR via Gazebo + TurtleBot3 when no recorded/real scan data is
available.

(Renamed from `mapping_slam` to match the `airmouse_<role>` package naming convention and
`ros2_ws/src/` layout in CLAUDE.md.)
