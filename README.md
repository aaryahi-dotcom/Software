# AirMouse-C

NIDAR 2026–27, Track 1: GPS-Denied Indoor Search & Rescue. An autonomous indoor drone
enters a covered maze arena with no GPS, navigates corridors and rooms, detects up to 6
survivors, builds a live 2D occupancy map, tags each survivor to a grid coordinate, and
exits — fully autonomously, in under 30 minutes.

See `CLAUDE.md` in the repo root for full project context, the five-role software split,
the topic contract, tech stack decisions, and the current phase (2-day software prototype,
no hardware yet). Read `docs/mission-brief.pdf` and `docs/airmouse-c-design-reference.pdf`
before touching scoring, failsafes, or the comms link.

## Layout

- `ros2_ws/src/` — one ROS 2 package per pipeline stage, plus `airmouse_interfaces`
  (shared message contract) and `airmouse_bringup` (single launch file for everything).
- `foxglove/` — ground station panel layout.
- `docs/` — mission brief, design reference, human-readable topic contract.
- `scripts/` — dev environment setup.
- `test_data/` — pointer to shared drive for rosbags/weights (never committed here).

## Getting started

```
./scripts/setup_dev.sh
```

See `CONTRIBUTING.md` for branch naming, PR checklist, and the git workflow.
