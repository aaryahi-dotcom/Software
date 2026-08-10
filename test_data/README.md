# Test data

Recorded rosbags, trained weights, and anything over a few MB are never committed to this
repo. They live on the shared drive instead.

Shared drive location: TBD — add the link here once the team has one.

Local convention: drop bags/weights under `test_data/` locally (it's gitignored via the
`*.db3` / `*.mcap` / `*.pt` patterns in the root `.gitignore`); don't create a nested
`test_data/.gitignore`, the root one already covers it.
