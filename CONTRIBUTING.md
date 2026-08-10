# Contributing

Keep this file in sync with the "Git workflow" section of `CLAUDE.md`.

## Branches

- `main` is branch-protected: no direct pushes, PR required, 1 approval required, no
  force push, no branch deletion bypass.
- No `develop` branch — branch straight off `main`.
- Branch naming: `role<n>/<short-description>`, e.g. `role3/temporal-confirmation`.

## Pull requests

- Keep PRs small, squash-merge, delete the branch on merge.
- PR checklist:
  - [ ] Runs locally without errors
  - [ ] Only touches files inside one role's package (or interface changes were flagged
        to the team)
  - [ ] Topic names match the contract table in `CLAUDE.md` / `docs/interfaces.md`
  - [ ] Commit message says what it does

## Interface changes

`airmouse_interfaces` is the shared message contract package. Changing a field type there
breaks the build for every consumer — that's intentional, it's the safety net. Flag any
change to the team before merging, and update `docs/interfaces.md` in the same PR.
