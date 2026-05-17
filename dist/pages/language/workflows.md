## [Workflows](#workflows-4)

| Statement | Syntax | Notes |
| --- | --- | --- |
| List workflows | `LIST WORKFLOWS [IN Module];` | List all or filter by module |
| Describe workflow | `DESCRIBE WORKFLOW Module.Name;` | Full MDL output |
| Create workflow | `CREATE [OR MODIFY] WORKFLOW Module.Name PARAMETER $Ctx: Module.Entity BEGIN ... END WORKFLOW;` | See activity types below |
| Drop workflow | `DROP WORKFLOW Module.Name;` |  |

**Workflow Activity Types:**

- `USER TASK <name> '<caption>' [PAGE Mod.Page] [TARGETING MICROFLOW Mod.MF] [OUTCOMES '<out>' { } ...];`
- `CALL MICROFLOW Mod.MF [COMMENT '<text>'] [OUTCOMES '<out>' { } ...];`
- `CALL WORKFLOW Mod.WF [COMMENT '<text>'];`
- `DECISION ['<caption>'] OUTCOMES '<out>' { } ...;`
- `PARALLEL SPLIT PATH 1 { } PATH 2 { };`
- `JUMP TO <activity-name>;`
- `WAIT FOR TIMER ['<expr>'];`
- `WAIT FOR NOTIFICATION;`
- `END;`

**Example:**

```
CREATE WORKFLOW Module.ApprovalFlow
  PARAMETER $Context: Module.Request
  OVERVIEW PAGE Module.WorkflowOverview
BEGIN
  USER TASK ReviewTask 'Review the request'
    PAGE Module.ReviewPage
    OUTCOMES 'Approve' { } 'Reject' { };
END WORKFLOW;

```