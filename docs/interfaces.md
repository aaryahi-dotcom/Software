# Topic contract

Human-readable mirror of the message contract defined in `airmouse_interfaces`. This is
the interface between the five software roles — do not rename a topic or change a field
type here without updating every subscriber and the `.msg`/`.srv` definitions in
`ros2_ws/src/airmouse_interfaces`.

| Topic | Message type | Publisher | Subscriber(s) |
|---|---|---|---|
| `/scan` | `sensor_msgs/LaserScan` | LiDAR (real or replayed) | Role 2 |
| `/map` | `nav_msgs/OccupancyGrid` | Role 2 | Role 4a/4b, Role 5 |
| `/tf` | `tf2_msgs/TFMessage` | Role 2 (pose) | Role 4a, Role 5 |
| `/detections` | `vision_msgs/Detection2DArray` | Role 3 | Role 4a |
| `/survivor_markers` | `visualization_msgs/MarkerArray` | Role 4a | Role 5 |
| `/mission_status` | custom `MissionProgress.msg` | Role 4b | Role 5 |
| `/mavros/state` | `mavros_msgs/State` | Role 1 | Role 5 |
| `/operator/cmd` | custom `OperatorCommand.msg` (arm/abort/recall) | Role 5 | Role 1 |
