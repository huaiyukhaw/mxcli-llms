# [Design Principles](#design-principles)

mxcli is not a thin wrapper over the `.mpr` format. It is a deliberate bet on a
particular way of letting coding agents build Mendix applications: the agent
writes a **compact, human-readable DSL**, and mxcli’s **deterministic layer**
turns that DSL into the many low-level mutations, validations, and tool calls a
real model change requires. The principles below explain the design choices that
follow from that bet, and why they differentiate mxcli from driving Studio Pro’s
tools directly.