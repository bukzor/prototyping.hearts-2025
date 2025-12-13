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
