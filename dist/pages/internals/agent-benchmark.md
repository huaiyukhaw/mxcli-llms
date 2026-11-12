# [Agent Dev-Loop Benchmark](#agent-dev-loop-benchmark)

An agent building an app runs mxcli hundreds of times, and waits for each run.
The agent dev-loop benchmark measures that wait directly: a fixed session of
mxcli commands, **one process per command**, timed from outside. There is no
model in the loop, so the same commit gives the same session every time.

It complements two other things rather than replacing them:

- the **read and decode budget tests** in the unit suite, which fail a pull
  request that makes a command open more unit files than a bound. They are
  exact, but they count reads, on a 370-unit project, for the commands someone
  already found slow;
- **`mxcli eval run`** with `diag session-report`, which measures a whole agent
  session — model calls, tokens, wall time — and therefore varies from run to
  run.

Design and rationale: `docs/11-proposals/PROPOSAL_agent_devloop_benchmark.md`.