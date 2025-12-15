# Project Structure

Workspace and module organization.

| Concept | POC | Production |
|---------|-----|------------|
| Library unit | Python package | Rust crate |
| Workspace | uv workspace | cargo workspace |
| Entry point | `__init__.py` | `lib.rs` |
| Submodule | module | module |

## Planned Packages/Crates

- engine — game rules and state
- bot — AI players
- server — FastAPI/axum backend
- renderer — TypeScript (may stay TS in production)

## POC Workspace Layout

```
hearts/
├── pyproject.toml          # workspace root
├── packages/
│   ├── engine/
│   │   ├── pyproject.toml
│   │   └── src/hearts_engine/
│   ├── bot/
│   │   ├── pyproject.toml
│   │   └── src/hearts_bot/
│   └── server/
│       ├── pyproject.toml
│       └── src/hearts_server/
```

Root `pyproject.toml`:
```toml
[project]
name = "hearts"
version = "0.0.1"

[tool.uv.workspace]
members = ["packages/*"]
```

Package `pyproject.toml` (e.g., engine):
```toml
[project]
name = "hearts-engine"
version = "0.0.1"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```
