## [Entity Access](#entity-access-2)

### [GRANT](#grant)

```
GRANT <Module>.<Role> ON <Module>.<Entity> (<rights>) [WHERE '<xpath>'];

```

Where `<rights>` is a comma-separated list of:

| Right | Description |
| --- | --- |
| `CREATE` | Allow creating new objects |
| `DELETE` | Allow deleting objects |
| `READ *` | Read all members |
| `READ (<attr>, ...)` | Read specific members only |
| `WRITE *` | Write all members |
| `WRITE (<attr>, ...)` | Write specific members only |

GRANT is **additive**: if the role already has an access rule on the entity, new rights are merged in. Existing permissions are never removed by a GRANT — only upgraded.

Examples:

```
-- Full access
GRANT Shop.Admin ON Shop.Customer (CREATE, DELETE, READ *, WRITE *);

-- Read-only
GRANT Shop.Viewer ON Shop.Customer (READ *);

-- Selective members
GRANT Shop.User ON Shop.Customer (READ (Name, Email), WRITE (Email));

-- With XPath constraint (doubled single quotes for string literals)
GRANT Shop.User ON Shop.Order (READ *, WRITE *)
  WHERE '[Status = ''Open'']';

-- Additive: adds Notes to existing read access without removing Name, Email
GRANT Shop.User ON Shop.Customer (READ (Notes));

```
### [REVOKE](#revoke)

Remove an entity access rule entirely, or revoke specific rights:

```
-- Full revoke (removes entire rule)
REVOKE <Module>.<Role> ON <Module>.<Entity>;

-- Partial revoke (downgrades specific rights)
REVOKE <Module>.<Role> ON <Module>.<Entity> (<rights>);

```

For partial revoke, `REVOKE READ (x)` sets member x access to None. `REVOKE WRITE (x)` downgrades member x from ReadWrite to ReadOnly. `REVOKE CREATE` / `REVOKE DELETE` removes the structural permission.

Examples:

```
-- Remove all access
REVOKE Shop.Viewer ON Shop.Customer;

-- Remove read access on a specific member
REVOKE Shop.User ON Shop.Customer (READ (Notes));

-- Downgrade write to read-only
REVOKE Shop.User ON Shop.Customer (WRITE (Email));

-- Remove delete permission only
REVOKE Shop.User ON Shop.Customer (DELETE);

```