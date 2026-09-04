# [Project Brain](#project-brain)

`mxcli brain` records the project knowledge mxcli **cannot** compute. Two halves:

- **Decisions** — why a pattern was chosen here, which marketplace version broke
  what, what a recurring mxbuild error means in *this* app.
- **The plan** — the requirements being built from, grouped into slices, when the
  source is a specification document, a prototype or a conversation.

The plan half exists because that source leaves **no trace in git**. A Word
document, a Figma file and a chat window are not an issue and not a commit
message, so hours of work can end with nothing recording what it was for — and a
session resuming tomorrow has no idea what it was building towards.

It is opt-in. A project without `docs/brain/` never hears about it. `mxcli`’s
bootstrap interview asks for requirements by default.