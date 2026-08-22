# [Test Formats](#test-formats)

`mxcli test` reads two file formats: `.test.mdl` for plain MDL tests, and
`.test.md` for tests embedded in documentation. Both describe the same thing — a
named test, some MDL to run against the app, and what must be true afterwards —
and both use the same [annotations](#test-annotations).

A test’s body calls into the app. It is not a script that builds a project: the
statements run against a booted runtime, and the assertions are about what they
returned or wrote.