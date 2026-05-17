## [ALTER ENTITY](#alter-entity-2)

Modifies an existing entity without full replacement.

| Operation | Syntax | Notes |
| --- | --- | --- |
| Add attributes | `ALTER ENTITY Module.Name ADD (Attr: Type [constraints]);` | One or more attributes |
| Drop attributes | `ALTER ENTITY Module.Name DROP (AttrName, ...);` |  |
| Modify attributes | `ALTER ENTITY Module.Name MODIFY (Attr: NewType [constraints]);` | Change type/constraints |
| Rename attribute | `ALTER ENTITY Module.Name RENAME OldName TO NewName;` |  |
| Add index | `ALTER ENTITY Module.Name ADD INDEX (Col1 [ASC|DESC], ...);` |  |
| Drop index | `ALTER ENTITY Module.Name DROP INDEX (Col1, ...);` |  |
| Set documentation | `ALTER ENTITY Module.Name SET DOCUMENTATION 'text';` |  |
| Set position | `ALTER ENTITY Module.Name SET POSITION (100, 200);` | Canvas position |

**Example:**

```
ALTER ENTITY Sales.Customer
  ADD (Phone: String(50), Notes: String(unlimited));

ALTER ENTITY Sales.Customer
  RENAME Phone TO PhoneNumber;

ALTER ENTITY Sales.Customer
  ADD INDEX (Email);

```