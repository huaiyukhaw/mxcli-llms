# [Test Annotations](#test-annotations)

Annotations describe what a test is and what must be true when it finishes. They
live in the javadoc comment above a test’s statements, one per line, each opening
its line:

```
/**
 * @test dealing a board writes 81 cells
 * @cleanup none
 * @expect $result = 'ok'
 * @verify select count(*) as n from Sudoku.Cell = 81
 */
$result = call microflow Sudoku.ACT_DealGame();
/

```

| Tag | Purpose |
| --- | --- |
| `@test <name>` | Names the test. Required — a doc comment without it is not a test. |
| `@expect <condition>` | A Mendix expression over the body’s variables that must be true. Repeatable. |
| `@verify <oql> <op> <value>` | An OQL post-condition on the database. Repeatable. |
| `@throws '<message>'` | The body is expected to raise an error. |
| `@setup <Module.Microflow>` | A microflow to call before the body. Repeatable. |
| `@cleanup rollback|none` | Whether the test’s writes survive it. `rollback` is the default. |

A tag is read only when it **opens its line** (after the javadoc `*` and its
indentation). Quoting one inside a sentence — ``@expect $x = 1`` — is
documentation, not an assertion.