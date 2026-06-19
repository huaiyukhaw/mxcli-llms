# [Graph Analysis](#graph-analysis)

mxcli models a Mendix project as a **dependency graph** — documents (entities,
microflows, pages, …) are nodes and their references (`CATALOG.REFS`) are edges —
and runs topological analyses on top of it: god nodes, module coupling, community
detection, dependency cycles, layering, and centrality.

Use it to **understand an unfamiliar app and decide where to intervene**: what’s
central and risky to change, which modules are entangled, what naturally belongs
together, and what it would take to split the app.

All of this is pure-Go (no external dependencies) and reads the catalog, so it
needs no Studio Pro and no cloud connectivity. It requires a **full** catalog
(the graph lives in the `refs` table, built by `refresh catalog full`).