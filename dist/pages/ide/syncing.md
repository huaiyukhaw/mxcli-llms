# [Syncing with Updates](#syncing-with-updates)

When you upgrade `mxcli`, the skills, lint rules and project guidance it ships
may have changed. A project keeps them in step with the binary through one
command, which the Claude Code bootstrap script runs on every session start:

```
mxcli init --sync-skills      # or: mxcli init --sync

```

It is quiet when everything is already current.