# 2025-12-15-001: Scaffold Complete

Session implementing the a000 scaffold plan.

## What Happened

Implemented project infrastructure per the scaffold plan in a000-local-prototype.md:

- Created uv workspace with 3 packages (engine, bot, renderer_cli)
- Set up pre-commit hooks: prettier, pyupgrade, isort, black, pyright
- Added CI workflow with test and pre-commit jobs
- Added Cargo.toml placeholder for future Rust migration
- Used src layout (`packages/engine/src/hearts_engine/`) to mirror Rust crate structure

## Deviations from Plan

- **Python 3.14** instead of 3.13 (uv picked latest available)
- **src layout** instead of flat layout (better mirrors Rust `crate/src/lib.rs`)
- **hatchling** build backend (simpler than setuptools for src layout)
- Added `py.typed` marker files for strict typing

## CI Verification

Created intentional test failure to verify CI catches failures:

- `pre-commit` job: passed
- `test` job: failed as expected

After removing intentional failure, both jobs pass.

## Files Created

```
.envrc
.github/workflows/pre-commit.yml
.pre-commit-config.yaml
Cargo.toml
bin/pnpm-run
package.json
pnpm-lock.yaml
pyproject.toml
packages/engine/pyproject.toml
packages/engine/src/hearts_engine/__init__.py
packages/engine/src/hearts_engine/py.typed
packages/engine/tests/__init__.py
packages/engine/tests/engine_test.py
packages/bot/pyproject.toml
packages/bot/src/hearts_bot/__init__.py
packages/bot/src/hearts_bot/py.typed
packages/renderer_cli/pyproject.toml
packages/renderer_cli/src/hearts_renderer_cli/__init__.py
packages/renderer_cli/src/hearts_renderer_cli/py.typed
```

## Next Steps

1. User review of scaffold
2. Implement engine — cards, hands, tricks, rules, scoring
3. Implement renderer_cli — display GameState, accept input
4. Implement bot — a000 heuristics
5. Wire together and playtest
