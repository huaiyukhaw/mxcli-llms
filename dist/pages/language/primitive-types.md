## [Primitive Types](#primitive-types-1)

| MDL Type | Description | Range/Limits |
| --- | --- | --- |
| `String` | Variable-length text (default length 200) | 1 to `unlimited` characters |
| `String(n)` | Variable-length text with explicit length | 1 to `unlimited` characters |
| `Integer` | 32-bit signed integer | -2,147,483,648 to 2,147,483,647 |
| `Long` | 64-bit signed integer | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 |
| `Decimal` | High-precision decimal number | Up to 20 digits total |
| `Boolean` | True/false value | `true` or `false` (must have DEFAULT) |
| `DateTime` | Date and time with timezone awareness | UTC timestamp |
| `Date` | Date only (no time component) | Internally stored as DateTime |
| `AutoNumber` | Auto-incrementing integer | Typically combined with NOT NULL UNIQUE |
| `Binary` | Binary data (files, images) | Configurable max size |
| `HashedString` | Securely hashed string (passwords) | One-way hash, cannot be retrieved |