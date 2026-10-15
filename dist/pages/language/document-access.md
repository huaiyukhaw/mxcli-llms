# [Microflow, Page, and Nanoflow Access](#microflow-page-and-nanoflow-access)

Document-level access controls which module roles can execute microflows and nanoflows or view pages. GRANT adds roles and REVOKE removes them; neither replaces the list.

A new page, microflow or nanoflow has no allowed roles until you grant some, in every module: mxcli never creates a module role on its own. In a module with no module roles yet, create one first (`create module role <Module>.User;`) and map it into a user role. See [GRANT](#default-access-of-a-new-page-microflow-or-nanoflow).