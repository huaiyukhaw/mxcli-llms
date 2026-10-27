# [Microflow Statements](#microflow-statements)

Statements for creating, altering and dropping microflows, nanoflows, and Java actions.

Microflows are the primary mechanism for implementing business logic in Mendix applications. They execute on the server and have access to the full range of activities including database operations, integrations, and security-sensitive actions.

Nanoflows share the same syntax as microflows but execute on the client (browser or native mobile). They have a restricted set of available activities.

| Statement | Description |
| --- | --- |
| [CREATE MICROFLOW](#create-microflow) | Create a microflow with activities and control flow |
| [CREATE NANOFLOW](#create-nanoflow) | Create a client-side nanoflow |
| [ALTER MICROFLOW / NANOFLOW](#alter-microflow--nanoflow) | Patch a stored flow in place: insert, replace or drop activities, or replace a loop’s body |
| [CREATE JAVA ACTION](#create-java-action) | Create a Java action stub with inline code |
| [DROP MICROFLOW / NANOFLOW](#drop-microflow--nanoflow) | Remove a microflow or nanoflow |