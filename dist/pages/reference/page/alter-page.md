## [ALTER PAGE / ALTER SNIPPET](#alter-page--alter-snippet-2)

Modify an existing page or snippet’s widget tree in-place without full `CREATE OR REPLACE`. Works directly on the raw BSON tree, preserving unsupported widget types.

| Operation | Syntax | Notes |
| --- | --- | --- |
| Set property | `SET Caption = 'New' ON widgetName` | Single property on a widget |
| Set multiple | `SET (Caption = 'Save', ButtonStyle = Success) ON btn` | Multiple properties at once |
| Page-level set | `SET Title = 'New Title'` | No ON clause for page properties |
| Insert after | `INSERT AFTER widgetName { widgets }` | Add widgets after target |
| Insert before | `INSERT BEFORE widgetName { widgets }` | Add widgets before target |
| Drop widgets | `DROP WIDGET name1, name2` | Remove widgets by name |
| Replace widget | `REPLACE widgetName WITH { widgets }` | Replace widget subtree |
| Pluggable prop | `SET 'showLabel' = false ON cbStatus` | Quoted name for pluggable widgets |
| Add variable | `ADD Variables $name: Type = 'expr'` | Add a page variable |
| Drop variable | `DROP Variables $name` | Remove a page variable |

**Supported SET properties:** Caption, Label, ButtonStyle, Class, Style, Editable, Visible, Name, Title (page-level), and quoted pluggable widget properties.

**Example:**

```
ALTER PAGE Module.EditPage {
  SET (Caption = 'Save & Close', ButtonStyle = Success) ON btnSave;
  DROP WIDGET txtUnused;
  INSERT AFTER txtEmail {
    TEXTBOX txtPhone (Label: 'Phone', Attribute: Phone)
  }
};

ALTER SNIPPET Module.NavMenu {
  SET Caption = 'Dashboard' ON btnHome
};

```

**Tip:** Run `DESCRIBE PAGE Module.PageName` first to see widget names.