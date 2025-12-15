# Package Management

Dependency resolution, building, running.

| | POC | Production |
|-|-----|------------|
| Tool | uv | cargo |
| Manifest | pyproject.toml | Cargo.toml |
| Workspaces | uv workspace | cargo workspace |

## Notes

- Both handle dependencies, building, running
- uv is relatively new; cargo is mature and battle-tested
- Workspace structure mirrors between implementations
