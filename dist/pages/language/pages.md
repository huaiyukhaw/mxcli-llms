## [Pages](#pages-5)

MDL uses explicit property declarations for pages:

| Element | Syntax | Example |
| --- | --- | --- |
| Page properties | `(Key: value, ...)` | `(Title: 'Edit', Layout: Atlas_Core.Atlas_Default)` |
| Page variables | `Variables: { $name: Type = 'expr' }` | `Variables: { $show: Boolean = 'true' }` |
| Widget name | Required after type | `TEXTBOX txtName (...)` |
| Attribute binding | `Attribute: AttrName` | `TEXTBOX txt (Label: 'Name', Attribute: Name)` |
| Variable binding | `DataSource: $Var` | `DATAVIEW dv (DataSource: $Product) { ... }` |
| Action binding | `Action: TYPE` | `ACTIONBUTTON btn (Caption: 'Save', Action: SAVE_CHANGES)` |
| Microflow action | `Action: MICROFLOW Name(Param: val)` | `Action: MICROFLOW Mod.ACT_Process(Order: $Order)` |
| Database source | `DataSource: DATABASE Entity` | `DATAGRID dg (DataSource: DATABASE Module.Entity)` |
| Selection binding | `DataSource: SELECTION widget` | `DATAVIEW dv (DataSource: SELECTION galleryList)` |
| CSS class | `Class: 'classes'` | `CONTAINER c (Class: 'card mx-spacing-top-large')` |
| Inline style | `Style: 'css'` | `CONTAINER c (Style: 'padding: 16px;')` |
| Design properties | `DesignProperties: [...]` | `CONTAINER c (DesignProperties: ['Spacing top': 'Large', 'Full width': ON])` |
| Width (pixels) | `Width: integer` | `IMAGE img (Width: 200)` |
| Height (pixels) | `Height: integer` | `IMAGE img (Height: 150)` |
| Page size | `PageSize: integer` | `DATAGRID dg (PageSize: 25)` |
| Pagination mode | `Pagination: mode` | `DATAGRID dg (Pagination: virtualScrolling)` |
| Paging position | `PagingPosition: pos` | `DATAGRID dg (PagingPosition: both)` |
| Paging buttons | `ShowPagingButtons: mode` | `DATAGRID dg (ShowPagingButtons: auto)` |

**DataGrid Column Properties:**

| Property | Values | Default | Example |
| --- | --- | --- | --- |
| `Attribute` | attribute name | (required) | `Attribute: Price` |
| `Caption` | string | attribute name | `Caption: 'Unit Price'` |
| `Alignment` | `left`, `center`, `right` | `left` | `Alignment: right` |
| `WrapText` | `true`, `false` | `false` | `WrapText: true` |
| `Sortable` | `true`, `false` | `true`/`false` | `Sortable: false` |
| `Resizable` | `true`, `false` | `true` | `Resizable: false` |
| `Draggable` | `true`, `false` | `true` | `Draggable: false` |
| `Hidable` | `yes`, `hidden`, `no` | `yes` | `Hidable: no` |
| `ColumnWidth` | `autoFill`, `autoFit`, `manual` | `autoFill` | `ColumnWidth: manual` |
| `Size` | integer (px) | `1` | `Size: 200` |
| `Visible` | expression string | `true` | `Visible: '$showColumn'` (page variable, not $currentObject) |
| `DynamicCellClass` | expression string | (empty) | `DynamicCellClass: 'if(...) then ... else ...'` |
| `Tooltip` | text string | (empty) | `Tooltip: 'Price in USD'` |

**Page Example:**

```
CREATE PAGE MyModule.Customer_Edit
(
  Params: { $Customer: MyModule.Customer },
  Title: 'Edit Customer',
  Layout: Atlas_Core.PopupLayout
)
{
  DATAVIEW dvCustomer (DataSource: $Customer) {
    TEXTBOX txtName (Label: 'Name', Attribute: Name)
    TEXTBOX txtEmail (Label: 'Email', Attribute: Email)
    COMBOBOX cbStatus (Label: 'Status', Attribute: Status)

    FOOTER footer1 {
      ACTIONBUTTON btnSave (Caption: 'Save', Action: SAVE_CHANGES, ButtonStyle: Primary)
      ACTIONBUTTON btnCancel (Caption: 'Cancel', Action: CANCEL_CHANGES)
    }
  }
}

```

**Supported Widgets:**

- Layout: `LAYOUTGRID`, `ROW`, `COLUMN`, `CONTAINER`, `CUSTOMCONTAINER`
- Input: `TEXTBOX`, `TEXTAREA`, `CHECKBOX`, `RADIOBUTTONS`, `DATEPICKER`, `COMBOBOX`
- Display: `DYNAMICTEXT`, `DATAGRID`, `GALLERY`, `LISTVIEW`, `IMAGE`, `STATICIMAGE`, `DYNAMICIMAGE`
- Actions: `ACTIONBUTTON`, `LINKBUTTON`, `NAVIGATIONLIST`
- Structure: `DATAVIEW`, `HEADER`, `FOOTER`, `CONTROLBAR`, `SNIPPETCALL`