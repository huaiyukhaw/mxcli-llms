## [Constraints](#constraints-1)

| Constraint | Syntax | Description |
| --- | --- | --- |
| Not Null | `NOT NULL` | Value is required |
| Not Null with Error | `NOT NULL ERROR MESSAGE 'message'` | Required with custom error |
| Unique | `UNIQUE` | Value must be unique |
| Unique with Error | `UNIQUE ERROR MESSAGE 'message'` | Unique with custom error |

Constraints must appear in this order:

1. `NOT NULL [ERROR '...']`
2. `UNIQUE [ERROR '...']`
3. `DEFAULT <value>`