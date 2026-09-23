## [Structure](#structure-1)

An MPR file is a standard SQLite database. Both format versions carry the same
two tables; v2 adds a third. Contents live in the `Unit` table in v1 and in
`mprcontents/` in v2 — **there is no separate contents table in either format.**

| Table | v1 | v2 | Holds |
| --- | --- | --- | --- |
| `Unit` | yes | yes | One row per document |
| `_MetaData` | yes | yes | Mendix product/build version and schema hash |
| `_Transaction` | no | yes | `LastTransactionID`, bumped on every unit write |

### [Unit Table](#unit-table)

The `Unit` table has one row per document. Its columns are identical in both
formats except for `Contents`, which only v1 has:

| Column | v1 | v2 | Description |
| --- | --- | --- | --- |
| `UnitID` | yes | yes | Binary UUID identifying the document (.NET GUID byte order — see below) |
| `ContainerID` | yes | yes | Parent unit’s `UnitID`; the project root is its own container |
| `ContainmentName` | yes | yes | Relationship name (e.g. `ProjectDocuments`), empty on the root |
| `TreeConflict` | yes | yes | Version-control conflict marker |
| `ContentsHash` | yes | yes | Base64 SHA-256 of the document BSON |
| `ContentsConflicts` | yes | yes | Version-control conflict marker for contents |
| `Contents` | **yes** | **no** | BSON blob containing the full document |

The row carries **no unit-type and no name column** — the seven above are all
there is. A document’s type and name are read out of its BSON `$Type` and
`Name` fields, which is why listing units by type requires decoding contents
(`getTypeFromContents` in `modelsdk/mpr/reader_units.go`).

### [Where Contents Live](#where-contents-live)

In **v1**, document BSON is the `Unit.Contents` blob:

```
SELECT Contents FROM Unit WHERE UnitID = ?;          -- read
UPDATE Unit SET Contents = ? WHERE UnitID = ?;       -- write

```

In **v2**, `Unit.Contents` does not exist. Each document is a file under
`mprcontents/`, sharded two levels deep by the first four hex characters of its
UUID:

```
mprcontents/<XX>/<YY>/<UUID>.mxunit

```

The UUID in the path is the `UnitID` blob rendered in **.NET GUID byte order** —
the first three fields are little-endian, so blob `FADF10BF FF61 8842 8A63D53AE4522615`
becomes `bf10dffa-61ff-4288-8a63-d53ae4522615`. Writing a v2 unit updates
`Unit.ContentsHash` (and `_Transaction.LastTransactionID`) in SQLite after the
file lands.