# [Testing](#testing)

mxcli includes a testing framework for a Mendix app’s own logic: each test calls
into the running app — a microflow, a retrieve — and asserts on what came back or
what was written. It is not a check that an MDL script parses; that is
[`mxcli check`](#validating-with-mxcli-check).