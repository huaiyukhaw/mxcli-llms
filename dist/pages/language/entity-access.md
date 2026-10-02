## [Entity Access](#entity-access-2)

### [GRANT](#grant)

```
GRANT <rights> ON ENTITY <Module>.<Entity> TO <Module>.<Role> [, ...] [WHERE [<xpath>]];

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
mdl 1;
-- Full access
GRANT CREATE, DELETE, READ *, WRITE * ON ENTITY Shop.Customer TO Shop.Admin;

-- Read-only
GRANT READ * ON ENTITY Shop.Customer TO Shop.Viewer;

-- Selective members
GRANT READ (Name, Email), WRITE (Email) ON ENTITY Shop.Customer TO Shop.User;

-- With XPath constraint (doubled single quotes for string literals)
GRANT READ *, WRITE * ON ENTITY Shop.Order TO Shop.User
  WHERE [Status = 'Open'];

-- Additive: adds Notes to existing read access without removing Name, Email
GRANT READ (Notes) ON ENTITY Shop.Customer TO Shop.User;

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
mdl 1;
-- Remove all access
REVOKE ALL ON ENTITY Shop.Customer FROM Shop.Viewer;

-- Remove read access on a specific member
REVOKE READ (Notes) ON ENTITY Shop.Customer FROM Shop.User;

-- Downgrade write to read-only
REVOKE WRITE (Email) ON ENTITY Shop.Customer FROM Shop.User;

-- Remove delete permission only
REVOKE DELETE ON ENTITY Shop.Customer FROM Shop.User;

```