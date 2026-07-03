## [ALTER ENTITY](#alter-entity-2)

Modifies an existing entity without full replacement.

| Operation | Syntax | Notes |
| --- | --- | --- |
| Add attribute | `ALTER ENTITY Module.Name ADD ATTRIBUTE Attr: Type [constraints];` | One action per statement |
| Drop attribute | `ALTER ENTITY Module.Name DROP ATTRIBUTE AttrName;` |  |
| Modify attribute | `ALTER ENTITY Module.Name MODIFY ATTRIBUTE Attr: NewType [constraints];` | Change type/constraints |
| Rename attribute | `ALTER ENTITY Module.Name RENAME ATTRIBUTE OldName TO NewName;` |  |
| Add index | `ALTER ENTITY Module.Name ADD INDEX [IdxName] (Col1 [ASC|DESC], ...);` | Name optional |
| Drop index | `ALTER ENTITY Module.Name DROP INDEX IdxName;` | By index name |
| Set documentation | `ALTER ENTITY Module.Name SET DOCUMENTATION 'text';` |  |
| Set position | `ALTER ENTITY Module.Name SET POSITION (100, 200);` | Canvas position |

**Example:**

```
ALTER ENTITY Sales.Customer ADD ATTRIBUTE Phone: String(50);
ALTER ENTITY Sales.Customer ADD ATTRIBUTE Notes: String(unlimited);

ALTER ENTITY Sales.Customer RENAME ATTRIBUTE Phone TO PhoneNumber;

ALTER ENTITY Sales.Customer ADD INDEX (Email);

```