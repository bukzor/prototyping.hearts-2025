<anthropic-skill-ownership llm-subtask />

# Immutability Refactor

**Priority:** High **Complexity:** Medium-High **Context:** Dependency graph
analysis in `tmp/dep_clusters.png`

## Problem Statement

Engine uses mutable dataclasses and collections. This makes reasoning about
state changes harder, prevents hashability (can't use states as dict keys), and
complicates potential undo/replay features.

## Current Situation (updated 2025-12-18)

Most dataclasses frozen. Remaining:

- `GameState` not frozen (uses `.copy()` for external immutability)
- `Hand` is mutable `set[Card]` (blocks full hashability)
- Local mutable collections in `passing.py`, `cards.py`
- Methods still on: `Trick`, `Cards`, `Deck`, `GameState`

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

- [~] **Phase 2: Collections**
  - [ ] `Hand` → `frozenset` (deferred - requires more changes)
  - [x] `list` → `tuple` for `players`, `tricks_won`, `pending_passes`
  - [ ] `Cards.group()` returns `dict[Suit, list[Card]]` → consider frozen
  - [ ] `Deck.deal_hands()` returns `list[Hand]` → `tuple[Hand, ...]`
  - [ ] `passing.py:70` uses `dict[PlayerId, list[Card]]` locally

- [~] **Phase 3: Freeze**
  - [x] `PlayerState` frozen with `update_player()` helper
  - [ ] `GameState` frozen (optional - copy-on-write provides external
        immutability)

- [ ] **Phase 4: Methods → Functions**
  - [ ] `Trick.with_play(player, card)` → `trick_with_play(trick, player, card)`
  - [ ] `Cards.draw(n, rng)` → `draw_cards(cards, n, rng)`
  - [ ] `Deck.deal_hands(rng)` → `deal_hands(deck, rng)` or just
        `deal_hands(rng)`
  - [ ] `GameState.copy()` → remove (replace() works for frozen)
  - [ ] Keep: self-only (`items`, `values`, `group`), alt constructors
        (`from_dict`), dunders

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
- [ ] All dataclasses frozen (including `GameState`)
- [ ] `Hand` → `frozenset` for full hashability
- [ ] No methods with non-self args (except alt constructors)
- [ ] Module structure matches dependency clusters
- [x] All tests pass
- [x] Types clean (pyright 0 errors)
