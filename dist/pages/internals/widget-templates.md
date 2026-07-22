# [Widget Template System](#widget-template-system)

Pluggable widgets (DataGrid2, ComboBox, Gallery, etc.) require embedded template definitions for correct BSON serialization. This page explains how the template system works, from extraction through runtime loading and property mapping.

> For the user-facing view — how mxcli keeps widget definitions version-correct across Mendix releases, and the `mxcli widget describe` command for inspecting a widget’s discovered properties and dynamic rules — see [Pluggable Widgets Across Versions](#pluggable-widgets-across-mendix-versions).