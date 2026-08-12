# [Idempotent Writes](#idempotent-writes)

Re-running an MDL script against a project that is already in sync leaves the
`.mpr` and `mprcontents/` files **byte-identical**. `git status` stays clean and
Studio Pro shows no version-control changes, because the write does not happen at
all.

This matters beyond tidiness: without it, `git diff` cannot answer “did this
script change anything”, two people running the same script commit different
bytes, and a `.mxunit` merge conflict is not resolvable by hand.