# airmouse_autonomy - Role 4b: Autonomy

Role 4b implements mission-level autonomy for the AirMouse system.

## Implemented Components

### Mission Manager

Handles mission state transitions:

IDLE -> EXPLORING -> SURVIVOR_FOUND -> RETURNING -> COMPLETE

The mission manager tracks survivor count, publishes mission status, and triggers return-to-entry behavior after survivor detection.

### Frontier Explorer

Consumes `/map` as `nav_msgs/OccupancyGrid` and detects frontier cells where known free space borders unknown space.

Frontier candidates are scored using local frontier density and distance from the map center. Repeated targets are suppressed.

Prototype output:

`/exploration_target` - `geometry_msgs/PoseStamped`

### Return-to-Entry

Stores the first received robot pose as the mission entry position.

When a `RETURN` command is received, the saved entry pose is published as the return target.

Prototype interfaces:

`/robot_pose` - `geometry_msgs/PoseStamped`

`/return_command` - `std_msgs/String`

`/return_to_entry` - `geometry_msgs/PoseStamped`

## Mission Status

The current prototype publishes `/mission_status` using `std_msgs/String`.

The repository interface contract specifies a future shared `MissionProgress.msg` interface. The message definition is not currently present in `airmouse_interfaces`, so the prototype retains `std_msgs/String` until the shared contract is implemented.

## Testing

Build the package with:

`cd ~/Software/ros2_ws`

`source /opt/ros/humble/setup.bash`

`colcon build --packages-select airmouse_autonomy`

`source install/setup.bash`

Available executables:

- `frontier_explorer`
- `mission_manager`
- `return_to_entry`

## Integration Notes

The autonomy nodes have been tested independently and together using ROS 2 topics.

Final integration should follow the shared interface contract documented in `docs/interfaces.md` and implemented through `airmouse_interfaces`.
