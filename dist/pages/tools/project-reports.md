# [Project Reports](#project-reports)

`mxcli report <kind>` produces a report a team asks of any Mendix app. Bare
`mxcli report` is still the scored best-practices report ([mxcli report](#mxcli-report));
the kinds below answer specific questions instead of scoring.

| Kind | Question it answers |
| --- | --- |
| `architecture` | How do the app’s modules depend on each other; where are the layers, bounded contexts and real cycles; what is unused? |
| `tests` | What do the microflow tests and browser journeys check, did they pass, and which microflows do they reach, per module? |
| `security` | Who can read what, which client-callable flows trust the caller, which defaults are unsafe? |
| `performance` | Where does time go in the main journeys at production volume, and did a fix help? |
| `traceability` | Is each requirement in the specification built, and what proves it? |