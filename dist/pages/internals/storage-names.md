# [Storage Names vs Qualified Names](#storage-names-vs-qualified-names-1)

Mendix uses different “storage names” in BSON `$Type` fields than the “qualified names” shown in the TypeScript SDK documentation. Using the wrong name causes a `TypeCacheUnknownTypeException` when opening the project in Studio Pro.