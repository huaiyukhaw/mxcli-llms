# [Exploring a Project](#exploring-a-project)

Once you have a project open – whether through the REPL, a CLI one-liner, or a script file – the next step is to look around. What modules exist? What entities are defined? What does a particular microflow do?

mxcli provides three families of commands for exploration:

- **SHOW** commands list elements by type. `SHOW ENTITIES` lists all entities; `SHOW MICROFLOWS IN Sales` narrows the list to one module.
- **DESCRIBE** commands display the full MDL source for a single element, giving you the complete definition including attributes, associations, logic, and widget trees.
- **SEARCH** performs full-text search across every string in the project – captions, messages, expressions, documentation, and more.
- **SHOW STRUCTURE** gives you a compact tree view of the entire project or a single module, at varying levels of detail.

These commands are read-only. They never modify your project. You can run them freely to build a mental model of the application before making any changes.