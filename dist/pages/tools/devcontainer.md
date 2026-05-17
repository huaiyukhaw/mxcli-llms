## [Dev Container Setup](#dev-container-setup-1)

When using `mxcli init`, a `.devcontainer/` configuration is also created. Opening the project in VS Code and choosing **Reopen in Container** gives you a sandboxed environment with:

| Component | Purpose |
| --- | --- |
| **mxcli** | Mendix CLI binary (copied into the project) |
| **MxBuild / mx** | Project validation and building |
| **JDK 21** | Required by MxBuild |
| **Docker-in-Docker** | Running Mendix apps locally |
| **Node.js** | Playwright testing support |
| **PostgreSQL client** | Database connectivity |
| **Claude Code** | AI coding assistant (auto-installed) |

The VS Code extension is automatically available inside the dev container.