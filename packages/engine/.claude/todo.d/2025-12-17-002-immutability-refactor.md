<anthropic-skill-ownership llm-subtask />

# Immutability Refactor

**Priority:** High **Complexity:** Medium-High **Context:** Dependency graph
analysis in `tmp/dep_clusters.png`

## Problem Statement

Engine uses mutable dataclasses and collections. This makes reasoning about
state changes harder, prevents hashability (can't use states as dict keys), and
complicates potential undo/replay features.

## Current Situation

- Dataclasses are mutable (no `frozen=True`)
- Uses `set`, `list`, `dict` for collections
- `Trick` is `dict[PlayerId, Card]`
- Methods mixed with functions

## Proposed Solution

Full immutability stack:

- `frozen=True` on all dataclasses
- `frozenset` / `tuple` for collections
- `frozendict` from PyPI where needed
- Custom `Trick` type with `__getitem__(PlayerId)`
- All methods → standalone functions (properties still allowed)
- Module reorganization to match dependency clusters

## Implementation Steps

- [ ] **Phase 1: Foundation**
  - [ ] Add `frozendict` dependency to pyproject.toml
  - [ ] Redesign `Trick` type (frozen dataclass with `__getitem__(PlayerId)`)

- [ ] **Phase 2: Collections**
  - [ ] `set` → `frozenset` throughout
  - [ ] `list` → `tuple` where appropriate
  - [ ] Audit remaining `dict` usages → `frozendict`

- [ ] **Phase 3: Freeze**
  - [ ] Add `frozen=True` to all dataclasses
  - [ ] Fix any mutation patterns surfaced (use `replace()`)

- [ ] **Phase 4: Functions**
  - [ ] Move all methods to standalone functions
  - [ ] Keep properties for computed attributes

- [ ] **Phase 5: Modules**
  - [ ] Reorganize to match cluster structure:
    - `play/` - card play validation
    - `actions/` - action types and dispatch
    - `passing/` - card passing phase
    - `ending/` - round/game completion + scoring
    - `start/` - initialization

## Open Questions

- Should `PlayerState.tricks_won` be `tuple[Trick, ...]` or stay as list?
- Module reorg: flat files or subpackages?

## Success Criteria

- [ ] All dataclasses frozen
- [ ] No mutable collections in type signatures
- [ ] All tests pass
- [ ] Dependency graph still clean (no new cycles)

## Notes

Suggested session breakdown:

- Session 1: Phases 1-2 (foundation + collections)
- Session 2: Phase 3 (freeze dataclasses, fix fallout)
- Session 3: Phases 4-5 (functions + module reorg)
