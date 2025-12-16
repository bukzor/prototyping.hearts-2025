---
status: active
---

# a000: Local Prototype

First playable version. Validates core game loop.

## Progress

See [.claude/todo.d/](../../.claude/todo.d/) for current work.

## Goals

- Play a complete game of Hearts that feels right
- Test game logic correctness
- Show someone else and they understand what this will become

## Scope

**In:**

- Pure Python (no server, engine via import)
- Python CLI renderer
- [Pass-the-controller](../features.kb/pass-the-controller.md) multiplayer (4
  players, 1 terminal)
- [Core rules](../rules.kb/) only (no JD variant)
- Basic [bot](../features.kb/bots.md) for playtesting (simple heuristics,
  opt-in)

**Out:**

- Networking
- Authentication
- Multiple browser sessions
- Optional rules
- Time controls
- Any UI polish

## Tech Stack

- Python 3.x with uv
- Python CLI renderer (no web UI in a000)
- Monorepo structure mimicking eventual Rust crates
- Renderer-agnostic:
  [GameState/PlayerAction interface](../dev/gamestate-interface.md)

## Package Structure

```
packages/
├── engine/           ← game rules, state
├── bot/              ← AI player
├── renderer_cli/     ← Python CLI, a000 primary
```

Server and web renderer (Preact/TS) deferred to a010.

## Success Criteria

Complete a 4-player game to 100 points with no rule violations.

## Getting Started

1. Set up uv workspace (see
   [project-structure](../tool-equivalence-classes.kb/project-structure.md))
2. Implement `engine/` — cards, hands, tricks, [rules](../rules.kb/),
   [scoring](../rules.kb/scoring.md)
3. Implement `renderer-cli/` — display
   [GameState](../dev/gamestate-interface.md), accept input
4. Implement `bot/` — [a000 heuristics](../features.kb/bots.md)
5. Wire together and play test

## Scaffold Plan

### Decisions

- **pyright** (not mypy) via pnpm
- **prettier** via `pnpm-run` wrapper
- **auto-commit** on CI (stefanzweifel/git-auto-commit-action)
- **underscores** for package names
- **Python 3.13**
- **`.envrc`** with `export REPO=$(git rev-parse --show-toplevel)`

### Files to Create

```
.envrc
.github/workflows/pre-commit.yml
.pre-commit-config.yaml
pyproject.toml
package.json
bin/pnpm-run
packages/engine/pyproject.toml
packages/engine/hearts_engine/__init__.py
packages/bot/pyproject.toml
packages/bot/hearts_bot/__init__.py
packages/renderer_cli/pyproject.toml
packages/renderer_cli/hearts_renderer_cli/__init__.py
```

### Reference Files

| Target                             | Source                                                        |
| ---------------------------------- | ------------------------------------------------------------- |
| `pyproject.toml` (root)            | `devinfra-flakiness/pyproject.toml`                           |
| `.pre-commit-config.yaml`          | `bukzor.color/.pre-commit-config.yaml` (drop rust hooks)      |
| `.github/workflows/pre-commit.yml` | `devinfra-metrics/.github/workflows/pre-commit.yml`           |
| `package.json`                     | `template.python-project/package.json`                        |
| `bin/pnpm-run`                     | `template.python-project/bin/pnpm-run`                        |
| `packages/*/pyproject.toml`        | `devinfra-flakiness/lib/flaky_test_automation/pyproject.toml` |

Reference paths: `~/repo/github.com/bukzor/work-stuff/repo/getsentry/` and
`~/repo/github.com/bukzor/template.python-project/`

### Pre-commit Hook Order

1. prettier (yaml, json, toml, md)
2. pyupgrade (--py313-plus)
3. isort
4. black
5. pyright (pass_filenames: false)
6. pre-commit-hooks (trailing-whitespace, end-of-file-fixer, check-yaml, etc.)

### Post-Creation

1. `uv sync`
2. `pnpm install`
3. `uv run pre-commit install`
4. `uv run pre-commit run --all-files`
