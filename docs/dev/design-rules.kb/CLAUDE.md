# Design Rules

Architectural constraints and coding standards for the engine package.

## What Belongs Here

- Immutability requirements and patterns
- Type safety constraints (frozen, Mapping vs dict, etc.)
- Code style rules beyond linter scope
- Patterns that prevent specific bug classes

## What Does NOT Belong

- Implementation details (those live in code)
- Task tracking (use `.claude/todo.d/`)
- API documentation (use docstrings)

## When to Add

Add a rule when:

- A constraint was established through discussion/refactoring
- The constraint isn't enforceable by linter/type checker alone
- Future agents need to know "we decided X because Y"
