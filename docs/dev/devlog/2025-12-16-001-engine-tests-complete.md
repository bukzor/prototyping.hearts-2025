# 2025-12-16-001: Engine Tests Complete

## Focus

TDD for remaining engine functions: trick completion, round scoring, moon
shooting, game end, new round.

## What Happened

**TDD cycle (proper):**

1. Broke 5 functions (`complete_trick`, `complete_round`, `apply_moon_choice`,
   `check_game_end`, `start_new_round`)
2. Wrote 12 tests that failed against broken code
3. Verified each failure was correct (right reason, right location)
4. Restored implementations
5. Fixed 1 test logic error (`round_scores` resets on new round; check
   cumulative `scores` instead)

**Stateful hypothesis tests added and proven:**

- `it_conserves_cards_through_passing` — caught card duplication (64 vs 52)
- `it_conserves_cards_through_tricks` — caught card loss (48 vs 52)
- `it_terminates_within_reasonable_actions` — caught infinite game (scores
  [146,110,114,98] still playing)

**Semantic fix:**

- Renamed `WINNING_SCORE` → `LOSING_SCORE` (in Hearts, points are bad)

## Decisions

- Tests must fail before they can be trusted
- Breaking code proves test exercises the right path

## What Works

Full game flow now tested:

- New game → passing → playing → trick completion → round scoring → game end
- Moon shooting choice (+26 to others or -26 to self)
- New round rotation (pass direction cycles)
- Card conservation invariants
- Game termination guarantee

## Test Count

70 tests, 0 failures, pyright clean.

## Next Session

1. CLI renderer (`packages/renderer_cli/`)
2. Bot for playtesting (`packages/bot/`)
3. Wire together for pass-the-controller play

## Files Changed

```
packages/engine/src/hearts_engine/
├── engine.py (LOSING_SCORE rename)
└── engine_test.py (+12 tests, +3 stateful hypothesis tests)
```
