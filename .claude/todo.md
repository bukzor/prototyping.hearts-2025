---
managed-by: Skill(llm-subtask)
cost-benefit-sweh:
  timebox:
    "@value": 5.0
    rationale: |
      a000 local prototype: ~3h CLI renderer package, ~1h two bot
      baselines, ~1h wire-together to a playable 4-player game.
      Engine complete (70 tests, pyright clean).
    confidence: tentative
  benefit-2w:
    "@value": 1.0
    rationale: |
      Hobby/learning project. Realistic 2w landing: CLI renderer
      structure + bot baselines started — partial progress toward
      playable milestone. ~1 SWEh-equivalent of forward value.
    confidence: tentative
  cost-of-delay-2w:
    "@value": 0.3
    rationale: |
      Low. Engine work landed 2025-12 — momentum already broken;
      additional 2w of pause is marginal. No money flow, no deadline.
      Decay risk: engine API recall when re-engaging.
    confidence: tentative
---

# Current Work

## Active: a000 Local Prototype

See `docs/milestones.kb/a000-local-prototype.md` for full scope.

### Next Up

- [ ] CLI renderer (`packages/renderer_cli/`)
- [ ] Bot for playtesting (`packages/bot/`)
- [ ] Wire together: playable 4-player pass-the-controller game

## Context

- Devlog: `docs/dev/devlog/2025-12-16-001-engine-tests-complete.md`
- 70 tests passing, pyright clean
- Engine complete: all game flow tested and verified via TDD
