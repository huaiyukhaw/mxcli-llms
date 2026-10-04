# [Writing Custom Rules](#writing-custom-rules)

You can extend the linter with your own rules written in Starlark, a Python-like
language. A rule is a `.star` file in the project’s `.claude/lint-rules/`
directory; `mxcli lint` (and the `lint` statement) load every file there next to
the built-in rules.

The complete rule API — every query builtin, every field of the structs they
return and the values those fields take — is documented in the
**`write-lint-rules` skill**, `.claude/skills/mendix/write-lint-rules/SKILL.md`,
which `mxcli init` installs into the project. That file is the reference; this
page shows the shape of a rule.