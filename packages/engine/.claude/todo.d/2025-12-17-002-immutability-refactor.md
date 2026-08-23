<anthropic-skill-ownership llm-subtask />

# Immutability Refactor

**Priority:** High **Complexity:** Medium-High **Context:** Dependency graph
analysis in `tmp/dep_clusters.png`

## Problem Statement

Engine uses mutable dataclasses and collections. This makes reasoning about
state changes harder, prevents hashability (can't use states as dict keys), and
complicates potential undo/replay features.

## Current Situation (updated 2025-12-23)

Phases 1-5 complete. Phase 6 Steps 1-5 complete.

Module pattern established:

- One function/class per file (e.g., `passing/apply_pass.py`)
- `api.py` in each package for public exports
- `__init__.py` empty (docstring only)
- External imports go through `package.api`
- Internal imports within package go direct

Completed packages: `types/`, `passing/`, `start/`, `ending/`. Top-level
`api.py` created for package-wide exports. Deleted `cards.py` (functions moved
to `start/`), `round.py` (functions moved to `ending/`).

Remaining: Phase 6 Steps 6-7.

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

- [x] **Phase 3: Freeze GameState**
  - [x] `PlayerState` frozen with `update_player()` helper
  - [x] `GameState` frozen - mutation functions return new state

- [x] **Phase 4: Narrow Function Signatures** Reduce coupling: functions should
      depend only on what they use. Work recursively - narrowing leaves reveals
      second-order opportunities.

  **Pass 1 - Leaf functions (no internal GameState deps):**
  - [x] `is_first_trick(state)` → `is_first_trick(tricks_won)`
  - [x] `can_lead_hearts(state)` → `can_lead_hearts(hand, hearts_broken)`
  - [x] `valid_pass_selections(state)` → `valid_pass_selections(hand)`
  - [x] `check_shot_moon(state)` → `check_shot_moon(tricks_won)`
  - [x] `next_player_for_passing(state)` →
        `next_player_for_passing(current_player, pending_passes)`

  **Pass 2 - Split valid_plays:**
  - [x] `valid_plays(hand, trick, ...)` → `valid_plays(hand, lead_suit, ...)`
  - [x] Extract `valid_leads(hand, first_trick, hearts_broken)`
  - [x] Extract `valid_follows(hand, lead_suit, first_trick)`
  - [x] Added `Trick.lead_suit` property

  **Remaining `state:` functions:** All are imperative shell (GameState →
  GameState transforms) or intentional adapters. No further narrowing needed.

- [x] **Phase 5: Types consolidation**
  - [x] Move ubiquitous types (Card, GameState, Phase, Rank) to `types/`
  - [x] Move collections (Cards, Hand, Trick) to `types/`
  - [x] Split into sub-package: card.py, cards.py, trick.py, player.py,
        phase.py, state.py, result.py, types.py (all under 100 LOC)
  - [x] Extract constants (TWO_OF_CLUBS, QUEEN_OF_SPADES) to `constants.py`
  - [x] Remove trivial `GameState.pass_direction` property

- [ ] **Phase 6: Module Reorganization** (detailed plan below)
  - [x] Step 1: `ending/scoring.py` (committed: 35fa2af)
  - [x] Step 2: `actions/play.py` (committed: 4dbd8dc)
  - [x] Step 3: `passing/` - split to one-function-per-file, added api.py
  - [x] Step 4: `start/` - created with Deck, deal_hands, new_game, etc.
  - [x] Step 5: `ending/` - split to one-function-per-file, added api.py
  - [ ] Step 6: `actions/`
  - [ ] Step 7: Cleanup (delete emptied modules)

## Phase 6 Detailed Plan

### Target Structure

```
hearts_engine/
  api.py           # top-level public exports
  actions/
    __init__.py    # empty (docstring only)
    api.py         # public exports
    play.py        # (existing - valid_plays, valid_leads, etc.)
    apply_play.py
    apply_action.py
    ...
  ending/
    __init__.py    # empty
    api.py         # public exports
    scoring.py     # (existing)
    complete_trick.py
    complete_round.py
    ...
  passing/
    __init__.py    # empty
    api.py         # public exports (done)
    apply_pass.py, execute_passes.py, ... (one per file, done)
  start/
    __init__.py    # empty
    api.py         # public exports (done)
    Deck.py, deal_hands.py, new_game.py, ... (one per file, done)
  types/
    __init__.py    # empty
    api.py         # public exports (done)
    card.py, cards.py, ... (done)
  constants.py     # (done)
  player.py        # Player protocol (stays)
  tty.py           # formatting (stays)
```

### Migration Order (leaf to root)

**Step 1: ending/scoring.py** ✓ (committed: 35fa2af)

- `card_points`, `trick_points`, `round_points` (from scoring.py)
- `apply_normal_scoring` (from round.py)
- Note: `is_point_card` goes to `actions/play.py`

**Step 2: actions/play.py**

- `is_point_card` (from scoring.py)
- `is_first_trick`, `valid_plays`, `valid_leads`, `valid_follows`
- `must_follow_suit`, `no_point_cards`, `no_hearts`, `two_of_clubs_only`
- `_apply_restrictions`

**Step 3: passing/**

- `pass_direction_for_round`, `pass_target`, `update_pending_passes` (from
  state.py)
- `apply_pass`, `next_player_for_passing`, `execute_passes` (from passing.py)

**Step 4: start/**

- `Deck`, `deal_hands`, `draw` (from cards.py)
- `find_two_of_clubs_holder` (from rules.py)
- `start_new_round` (from round.py)
- `new_game` (from main.py)
- `start_playing_phase` (from passing.py)

**Step 5: ending/**

- `trick_winner`, `check_shot_moon` (from rules.py)
- `complete_trick` (from play.py)
- `complete_round`, `apply_moon_choice`, `check_game_end` (from round.py)

**Step 6: actions/**

- `apply_action` (from main.py)
- `apply_play` (from play.py)
- `SelectPass`, `PlayCard`, `ChooseMoonOption` (from state.py)
- `valid_actions`, `valid_actions_for_state`, `valid_pass_selections` (from
  rules.py)

**Step 7: Cleanup**

- Delete emptied modules: `scoring.py`, `rules.py`, `round.py`, `play.py`,
  `cards.py`, `main.py`
- Keep: `state.py` (if `update_player` remains), `passing.py` (if anything
  remains)
- Update `__init__.py` exports and all test imports

### Per-Step Process

1. Create target module with moved functions
2. Update imports within moved functions
3. Update imports in all dependent modules (including tests)
4. Run tests
5. Delete emptied source file when fully migrated

### Cross-Cutting Concerns

- `draw_three`: Test helper only - move to `start/` (tests can import from
  there)
- `update_player`: Used by round, passing, play - keep in `state.py` as
  cross-cutting utility

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
- [x] All dataclasses frozen (including `GameState`)
- [x] `Hand` → `frozenset` for full hashability
- [~] No methods with non-self args (except alt constructors) - relaxed: filter
  methods like `of_suit()` kept as more Pythonic
- [ ] Module structure matches dependency clusters
- [x] All tests pass
- [x] Types clean (pyright 0 errors)
