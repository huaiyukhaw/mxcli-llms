# [Agent Editor Statements](#agent-editor-statements)

Statements for managing AI agent editor documents. Requires Mendix 11.9+ and the `AgentEditorCommons` module.

The Mendix Agent Editor introduces four document types that must be set up in dependency order:

1. **Model** — an LLM configuration referencing a Mendix Cloud GenAI Portal resource key
2. **Knowledge Base** — a vector knowledge base for retrieval-augmented generation
3. **Consumed MCP Service** — an external tool server (Model Context Protocol)
4. **Agent** — an AI agent that references a model and optionally uses knowledge bases and MCP services