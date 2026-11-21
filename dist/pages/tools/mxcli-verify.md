# [mxcli verify](#mxcli-verify)

`mxcli verify` is the one command that answers “did my change break anything?”. It runs the
checks in cost order and reports only the findings that are **new** against a baseline, so on
a mature project the result is about the change just made, not the backlog.

| Stage | What it runs | Against |
| --- | --- | --- |
| `check` | `mxcli check` on the script files you pass | nothing: every finding is the script’s |
| `exec` | `mxcli exec` on those scripts; only with `--apply`, and only if `check` passed | nothing: it applies the change |
| `lint` | `mxcli lint` on the project | `verify-baseline/lint.json` |
| `mxcheck` | `mx check` on a copy of the project | `verify-baseline/mxcheck.json` |

`mx check` is the authority. `mxcli check` cannot yet predict everything it rejects, so a project
that passes `check` and `lint` can still fail `mxcheck`; that is why the stage is part of the gate.