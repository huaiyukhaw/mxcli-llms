## [Project Settings](#project-settings-1)

| Statement | Syntax | Notes |
| --- | --- | --- |
| List settings | `LIST SETTINGS;` | Overview of all settings parts |
| Describe settings | `DESCRIBE SETTINGS;` | Full MDL output (round-trippable) |
| Alter model settings | `ALTER SETTINGS MODEL Key = Value;` | AfterStartupMicroflow, HashAlgorithm, JavaVersion, etc. |
| Alter configuration | `ALTER SETTINGS CONFIGURATION 'Name' Key = Value;` | DatabaseType, DatabaseUrl, HttpPortNumber, etc. |
| Alter constant | `ALTER SETTINGS CONSTANT 'Name' VALUE 'val' IN CONFIGURATION 'cfg';` | Override constant per configuration |
| Alter language | `ALTER SETTINGS LANGUAGE Key = Value;` | DefaultLanguageCode |
| Alter workflows | `ALTER SETTINGS WORKFLOWS Key = Value;` | UserEntity, DefaultTaskParallelism |