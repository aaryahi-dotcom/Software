#!/usr/bin/env bash
# Dev environment setup for AirMouse-C. Assumes ROS 2 Humble is already installed
# (Ubuntu 22.04, ARM64 where relevant) — see CLAUDE.md for the tech stack.
set -euo pipefail

cd "$(dirname "$0")/../ros2_ws"

rosdep update
rosdep install --from-paths src --ignore-src -r -y

colcon build --symlink-install

echo "Done. Source with: source install/setup.bash"
