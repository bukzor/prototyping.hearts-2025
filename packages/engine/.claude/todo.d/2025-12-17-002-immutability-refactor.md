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

- [x] **Phase 1: Foundation**
  - [x] ~~Add `frozendict` dependency~~ (not needed - used tuple pattern
        instead)
  - [x] Redesign `Trick` type (frozen dataclass with `__getitem__(PlayerId)`)

- [x] **Phase 2: Collections**
  - [ ] `Hand` → `frozenset` (deferred - requires more changes)
  - [x] `list` → `tuple` for `players`, `tricks_won`, `pending_passes`
  - [x] ~~Audit remaining `dict` usages~~ (only local vars, not stored state)

- [~] **Phase 3: Freeze**
  - [x] `PlayerState` frozen with `update_player()` helper
  - [ ] `GameState` frozen (optional - copy-on-write provides external
        immutability)

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

## Decisions Made

- `PlayerState.tricks_won`: chose `tuple[Trick, ...]`
- `pending_passes`: `tuple[tuple[Card,Card,Card]|None, ...]` indexed by PlayerId
- No `frozendict` needed - tuple patterns work for all stored state
- `Hand` stays as `set[Card]` for now (prevents full hashability)

## Success Criteria

- [x] Core dataclasses frozen (`Card`, `Trick`, `PlayerState`, actions)
- [x] No mutable collections in type signatures (except `Hand`)
- [x] All tests pass (105 tests)
- [x] Types clean (pyright 0 errors)

## Notes

Suggested session breakdown:

- Session 1: Phases 1-2 (foundation + collections)
- Session 2: Phase 3 (freeze dataclasses, fix fallout)
- Session 3: Phases 4-5 (functions + module reorg)
