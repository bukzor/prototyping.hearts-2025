# Project Structure

| Python | Rust |
|--------|------|
| package | crate |
| uv workspace | cargo workspace |
| `__init__.py` | `lib.rs` |
| module | module |

## Notes

- Python packages map to Rust crates
- Workspace structure should mirror between implementations
- Planned packages/crates: engine, bot, server, client

## uv Workspace Setup (POC)

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
