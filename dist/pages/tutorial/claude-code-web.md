# [Developing on the Web (Claude Code)](#developing-on-the-web-claude-code)

You can build a Mendix app with mxcli **entirely in the browser** — no local CLI,
no Studio Pro, no machine setup. [Claude Code on the web](https://claude.ai/code)
runs the agent in a cloud container against a GitHub repository; mxcli provisions
the whole toolchain inside that container on first run and commits the result so
future sessions come back up on their own. It works from a laptop, and from an
iPad or phone.

This page walks the **entire workflow**:

1. [Create a GitHub repository](#1-create-a-github-repository)
2. [Get a hub key for browser preview](#2-get-a-hub-key-for-browser-preview) (optional)
3. [Create a Claude Code environment](#3-create-a-claude-code-environment)
4. [Start the session with the bootstrap prompt](#4-start-the-session-with-the-bootstrap-prompt)
5. [Iterate — the warm loop, preview, and screenshots](#5-iterate)

> **New to how Claude Code on the web works** (sessions, environments, network
> policies)? See Anthropic’s guide:
> <https://code.claude.com/docs/en/claude-code-on-the-web>.