# [Microflow, Page, and Nanoflow Access](#microflow-page-and-nanoflow-access)

Document-level access controls which module roles can execute microflows and nanoflows or view pages. GRANT adds roles and REVOKE removes them; neither replaces the list.

A new document’s starting access depends on its module. In a module with no module roles, mxcli creates `<Module>.User` and grants every new page, microflow and nanoflow to it (`exec` prints `access: granted to auto-created role <Module>.User …` under the create), and a later GRANT adds to that rather than replacing it — revoke `<Module>.User` to narrow access. In a module with roles of its own, a new document has no allowed roles until you grant some. See [GRANT](#default-access-of-a-new-page-microflow-or-nanoflow).