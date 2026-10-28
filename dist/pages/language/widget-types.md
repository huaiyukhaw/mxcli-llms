# [Widget Types](#widget-types)

A widget is declared with a type keyword, a unique name, properties in parentheses, and optional child widgets in braces.

```
WIDGET_TYPE widgetName (Property: value, ...) [{ children }]

```

**Each built-in widget takes its own properties.** A property the widget does not take — `Caption:` on a `TEXTBOX` (an input’s label is `Label:`), `Label:` on an `ACTIONBUTTON`, `Visible:` on a `SNIPPETCALL` (Mendix stores no visibility for one), a misspelt key — is refused under `mdl 1;` by `check` and by `exec`, with nothing written (MDL-WIDGET52). Without the header it is dropped as before and warned about (MDL-V1-WIDGETPROP). The message lists the properties that widget takes.

**The list below is not the boundary.** The built-in Mendix widgets are documented here because they have fixed, hand-written property sets. Every **pluggable or custom widget** installed in the project is also written by its own name, with a body derived from the widget’s definition — see [Any installed widget](#any-installed-widget) below. If a widget is in `widgets/`, MDL can name it.