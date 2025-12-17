# Current Work

## Active: a000 Local Prototype

See `docs/milestones.kb/a000-local-prototype.md` for full scope.

### Engine (in progress)

- [ ] Test round completion (TDD)
  - [ ] Full trick flow (4 cards → winner takes)
  - [ ] Full round flow (13 tricks → scoring)
  - [ ] Moon shooting detection + choice
  - [ ] Game end at 100 points
  - [ ] New round start (re-deal, rotate pass direction)
- [ ] Stateful hypothesis tests
  - [ ] Random valid action sequences don't crash
  - [ ] Card conservation: hands + trick + tricks_won = 52
  - [ ] Games always reach GAME_END

### Remaining a000 deliverables

- [ ] CLI renderer (`packages/renderer_cli/`)
- [ ] Bot for playtesting (`packages/bot/`)
- [ ] Wire together: playable 4-player pass-the-controller game

## Context

- Devlog: `docs/dev/devlog/2025-12-16-000-engine-core.md`
- 56 tests passing, pyright clean
- Tests verified by intentional breakage
