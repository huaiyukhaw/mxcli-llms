# [Domain Model Layout](#domain-model-layout)

A domain model generated from an MDL script has to be *placed* somewhere, and
MDL says nothing about placement unless you write `@position` on every entity.
`mxcli layout` arranges a module from its association graph, so you do not have
to.

```
mxcli layout -p app.mpr --module Sales --dry-run   # list the moves
mxcli layout -p app.mpr --module Sales             # apply them
mxcli layout -p app.mpr                            # every module the project owns

```