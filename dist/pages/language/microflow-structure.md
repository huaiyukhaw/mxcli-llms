## [Structure](#structure-1)

An MPR file is a standard SQLite database with two key tables:

### [Unit Table](#unit-table)

The `Unit` table stores document metadata:

| Column | Description |
| --- | --- |
| `UnitID` | Binary UUID identifying the document |
| `ContainerID` | Parent module UUID |
| `ContainmentName` | Relationship name (e.g., `documents`) |
| `UnitType` | Fully qualified type name |
| `Name` | Document name |

### [UnitContents Table (v1 only)](#unitcontents-table-v1-only)

In MPR v1, the `UnitContents` table stores the actual BSON document content:

| Column | Description |
| --- | --- |
| `UnitID` | Binary UUID matching the Unit table |
| `Contents` | BSON blob containing the full document |

In MPR v2, document contents are stored as individual files in the `mprcontents/` folder instead.