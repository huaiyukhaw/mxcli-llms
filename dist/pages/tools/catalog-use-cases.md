## [Use Cases](#use-cases-4)

### [Verifying Imported Data](#verifying-imported-data)

After running `IMPORT FROM`, verify the data was imported correctly:

```
mxcli oql -p app.mpr "SELECT COUNT(*) FROM HR.Employee"
mxcli oql -p app.mpr "SELECT Name, Email FROM HR.Employee LIMIT 10"

```
### [Debugging Business Logic](#debugging-business-logic)

Check data state while debugging microflows:

```
mxcli oql -p app.mpr "SELECT * FROM Sales.Order WHERE Status = 'Draft'"

```
### [Data Exploration](#data-exploration)

Explore data patterns in a running application:

```
mxcli oql -p app.mpr "SELECT Status, COUNT(*) FROM Sales.Order GROUP BY Status"

```