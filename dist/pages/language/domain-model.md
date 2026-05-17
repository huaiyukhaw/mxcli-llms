## [Domain Model](#domain-model-4)

| Statement | Syntax | Notes |
| --- | --- | --- |
| Create entity | `CREATE [OR MODIFY] PERSISTENT|NON-PERSISTENT ENTITY Module.Name (attrs);` | Persistent is default |
| Create with extends | `CREATE PERSISTENT ENTITY Module.Name EXTENDS Parent.Entity (attrs);` | EXTENDS before `(` |
| Create view entity | `CREATE VIEW ENTITY Module.Name (attrs) AS SELECT ...;` | OQL-backed read-only |
| Create external entity | `CREATE EXTERNAL ENTITY Module.Name FROM ODATA CLIENT Module.Client (...) (attrs);` | From consumed OData |
| Create external entities | `CREATE [OR MODIFY] EXTERNAL ENTITIES FROM Module.Client [INTO Module] [ENTITIES (...)];` | Bulk from $metadata |
| Drop entity | `DROP ENTITY Module.Name;` |  |
| Describe entity | `DESCRIBE ENTITY Module.Name;` | Full MDL output |
| List entities | `LIST ENTITIES [IN Module];` | List all or filter by module |
| Create enumeration | `CREATE [OR MODIFY] ENUMERATION Module.Name (Value1 'Caption', ...);` |  |
| Drop enumeration | `DROP ENUMERATION Module.Name;` |  |
| Create association | `CREATE ASSOCIATION Module.Name FROM Parent TO Child TYPE Reference|ReferenceSet [OWNER Default|Both] [DELETE_BEHAVIOR ...];` |  |
| Drop association | `DROP ASSOCIATION Module.Name;` |  |