<anthropic-skill-ownership llm-subtask />

# Immutability Refactor

**Priority:** High **Complexity:** Medium-High **Context:** Dependency graph
analysis in `tmp/dep_clusters.png`

## Problem Statement

Engine uses mutable dataclasses and collections. This makes reasoning about
state changes harder, prevents hashability (can't use states as dict keys), and
complicates potential undo/replay features.

## Current Situation (updated 2025-12-19)

Most dataclasses frozen. `Hand`/`Cards` now frozenset-based. Remaining:

- `GameState` not frozen (uses `.copy()` for external immutability)
- Methods still on: `Trick`, `Cards`, `Deck`, `GameState`
- Validation functions now return `Iterator[Card]` (bonus refactor)

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
  - [x] `Cards` → `frozenset[Card]` (Hand inherits)
  - [x] `list` → `tuple` for `players`, `tricks_won`, `pending_passes`
  - [x] Added `Cards.of_suit()`, `not_of_suit()`, `hearts()` filter methods
  - [x] `Deck.deal_hands()` returns `Iterator[Hand]` (better than tuple)
  - [~] `Cards.group()` returns `dict[Suit, list[Card]]` - view method, low
    priority

- [ ] **Phase 3: Freeze GameState**
  - [x] `PlayerState` frozen with `update_player()` helper
  - [ ] `GameState` frozen - mutation functions must return new state

- [~] **Phase 4: Narrow Function Signatures** Reduce coupling: functions should
  depend only on what they use. Work recursively - narrowing leaves reveals
  second-order opportunities.

  **Pass 1 - Leaf functions (no internal GameState deps):**
  - [x] `is_first_trick(state)` → `is_first_trick(players)`
  - [x] `can_lead_hearts(state)` → `can_lead_hearts(hand, hearts_broken)`
  - [x] `valid_pass_selections(state)` → `valid_pass_selections(hand)`
  - [x] `check_shot_moon(state)` → `check_shot_moon(players)`
  - [x] `next_player_for_passing(state)` →
        `next_player_for_passing(current_player, pending_passes)`

  **Later passes:** TBD - discover as Pass 1 completes

- [ ] **Phase 5: Types consolidation**
  - [ ] Move "ubiquitous" types to `hearts_engine.types`
  - [ ] Use a sub-package if we near 300 LOC

- [ ] **Phase 6: Modules**
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
- `Cards` uses `frozenset[Card]` with `__sub__` override preserving subclass
  type
- Validation functions (`valid_leads`, `valid_plays`, etc.) return
  `Iterator[Card]`

## Success Criteria

- [x] Core dataclasses frozen (`Card`, `Trick`, `PlayerState`, actions)
- [ ] All dataclasses frozen (including `GameState`)
- [x] `Hand` → `frozenset` for full hashability
- [ ] No methods with non-self args (except alt constructors)
- [ ] Module structure matches dependency clusters
- [x] All tests pass
- [x] Types clean (pyright 0 errors)
