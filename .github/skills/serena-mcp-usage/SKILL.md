---
name: serena-mcp-usage
description: Improve task completion with Serena MCP in AniTrend. Use when you need to locate symbols, understand code structure, or make precise edits with symbol-aware tools instead of full-file reads.
compatibility: Requires Serena MCP symbol tools in a filesystem-based agent with access to the repo workspace.
---

# Serena MCP Usage for AniTrend

## When to use this skill
- You need to locate or edit specific classes, functions, or methods.
- You need quick structure without reading entire files.
- You must update all references after a change.

## Preferred workflow
1. Start with a symbol overview to understand file structure.
2. Use symbol search when you know (or can approximate) a name.
3. Use pattern search only when you do not know the symbol name.
4. Edit at symbol-level when changing whole methods/classes.
5. Use file-based edits only for small, localized changes.

## Step-by-step
1. Identify relevant files or modules.
2. Get symbols overview for the file(s).
3. Find the specific symbol and read only its body.
4. If changing a symbol, find referencing symbols and update usages.
5. Apply the smallest edits needed and keep style consistent.
6. Re-check for related symbols or imports that need updates.

## Common pitfalls
- Reading entire files before checking symbols.
- Editing a method without updating all references.
- Making broad file edits when a symbol edit would be more precise.

## Examples
- Update a use case method: overview → find symbol → replace symbol body → update references.
- Add a new resolver: overview → insert before/after symbol → check references.

## Notes for this repo
- Prefer module patterns from media/ as a reference.
- Keep code style aligned with existing conventions (typing, docstrings).
