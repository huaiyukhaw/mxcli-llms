# [Widget Types](#widget-types)

A widget is declared with a type keyword, a unique name, properties in parentheses, and optional child widgets in braces.

```
WIDGET_TYPE widgetName (Property: value, ...) [{ children }]

```

**The list below is not the boundary.** The built-in Mendix widgets are documented here because they have fixed, hand-written property sets. Every **pluggable or custom widget** installed in the project is also written by its own name, with a body derived from the widget’s definition — see [Any installed widget](#any-installed-widget) below. If a widget is in `widgets/`, MDL can name it.