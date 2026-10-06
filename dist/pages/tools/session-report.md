# [Measuring Agent Sessions](#measuring-agent-sessions)

An agent session’s cost is roughly **model calls × conversation size**: every
model call re-reads the whole conversation, and every tool result stays in it.
So a call removed takes its result with it, and the bill falls with the square
of the call count. Two commands measure where a session’s calls went:

| Command | Reads | Sees |
| --- | --- | --- |
| `mxcli diag loop-report` | mxcli’s own logs (`~/.mxcli/logs`) | mxcli processes: verbs, wall time, exits |
| `mxcli diag session-report` | the agent’s transcript | every tool call, its result size, failures and retries, tokens |

`loop-report` cannot see the agent’s Read/Edit/Grep/Skill calls, how large a
result was, or why a call happened. `session-report` can, because the
transcript records all of it.