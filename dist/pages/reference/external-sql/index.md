## [External SQL Statements](#external-sql-statements-1)

Direct SQL query execution against external databases (PostgreSQL, Oracle, SQL Server). Credentials are isolated – DSN never appears in session output or logs.

| Statement | Syntax | Notes |
| --- | --- | --- |
| Connect | `SQL CONNECT <driver> '<dsn>' AS <alias>;` | Drivers: `postgres`, `oracle`, `sqlserver` |
| Disconnect | `SQL DISCONNECT <alias>;` | Closes connection |
| List connections | `SQL CONNECTIONS;` | Shows alias + driver only (no DSN) |
| Show tables | `SQL <alias> SHOW TABLES;` | Lists user tables |
| Show views | `SQL <alias> SHOW VIEWS;` | Lists user views |
| Show functions | `SQL <alias> SHOW FUNCTIONS;` | Lists functions and procedures |
| Describe table | `SQL <alias> DESCRIBE <table>;` | Shows columns, types, nullability |
| Query | `SQL <alias> <any-sql>;` | Raw SQL passthrough |
| Import | `IMPORT FROM <alias> QUERY '<sql>' INTO Module.Entity MAP (...) [LINK (...)] [BATCH n] [LIMIT n];` | Insert external data into Mendix app DB |
| Generate connector | `SQL <alias> GENERATE CONNECTOR INTO <module> [TABLES (...)] [VIEWS (...)] [EXEC];` | Generate Database Connector MDL from schema |

```
-- Connect to PostgreSQL
SQL CONNECT postgres 'postgres://user:pass@localhost:5432/mydb' AS source;

-- Explore schema
SQL source SHOW TABLES;
SQL source DESCRIBE users;

-- Query data
SQL source SELECT * FROM users WHERE active = true LIMIT 10;

-- Import external data into Mendix app database
IMPORT FROM source QUERY 'SELECT name, email FROM employees'
  INTO HRModule.Employee
  MAP (name AS Name, email AS Email);

-- Import with association linking
IMPORT FROM source QUERY 'SELECT name, dept_name FROM employees'
  INTO HR.Employee
  MAP (name AS Name)
  LINK (dept_name TO Employee_Department ON Name);

-- Generate Database Connector from schema
SQL source GENERATE CONNECTOR INTO HRModule;
SQL source GENERATE CONNECTOR INTO HRModule TABLES (employees, departments) EXEC;

-- Manage connections
SQL CONNECTIONS;
SQL DISCONNECT source;

```

CLI subcommand: `mxcli sql --driver postgres --dsn '...' "SELECT 1"` (see `mxcli syntax sql`). Supported drivers: `postgres` (pg, postgresql), `oracle` (ora), `sqlserver` (mssql).