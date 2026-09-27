# [Microflow and Nanoflow Layout](#microflow-and-nanoflow-layout)

`mxcli layout flows` re-arranges existing microflows and nanoflows on their
canvas. It is the flow counterpart of [`mxcli layout`](#domain-model-layout),
and it is how you “reset the layout” of a flow: there is no clause on
`CREATE MICROFLOW` for that, because layout is not part of what a flow *does*.

```
mxcli layout flows -p app.mpr Sales.ACT_Order_Submit        # one flow
mxcli layout flows -p app.mpr --module Sales --dry-run      # list what would move
mxcli layout flows -p app.mpr --module Sales                # every flow in a module

```