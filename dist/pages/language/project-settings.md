## [Project Settings](#project-settings-1)

| Statement | Syntax | Notes |
| --- | --- | --- |
| Describe settings | `DESCRIBE SETTINGS;` | All settings parts, as MDL |
| Describe settings | `DESCRIBE SETTINGS;` | Full MDL output (round-trippable) |
| Alter runtime settings | `ALTER SETTINGS RUNTIME (Key: Value, ...);` | AfterStartupMicroflow, HashAlgorithm, JavaVersion, etc. |
| Alter configuration | `ALTER SETTINGS CONFIGURATION 'Name' (Key: Value, ...);` | DatabaseType, DatabaseUrl, HttpPortNumber, etc. |
| Alter constant | `ALTER SETTINGS CONSTANT @Module.Name VALUE 'val' IN CONFIGURATION 'cfg';` | Override constant per configuration |
| Alter language | `ALTER SETTINGS LANGUAGE (Key: Value);` | DefaultLanguageCode |
| Alter workflows | `ALTER SETTINGS WORKFLOWS (Key: Value, ...);` | UserEntity, DefaultTaskParallelism |