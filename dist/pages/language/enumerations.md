## [Enumerations](#enumerations-1)

```
reader.ListEnumerations()        // ([]*model.Enumeration, error) -- all enumerations

```

Each enumeration contains:

- `Name` – enumeration name
- `Values` – slice of `*model.EnumerationValue` with `Name` and `Caption`