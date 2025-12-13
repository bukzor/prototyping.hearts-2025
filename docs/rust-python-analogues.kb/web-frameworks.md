# Web Frameworks

| Python | Rust |
|--------|------|
| FastAPI | axum |
| uvicorn | tokio (runtime) |

## Notes

- Both async-first
- axum is tower-based, composes middleware similarly
- FastAPI's automatic OpenAPI docs don't have direct axum equivalent
- WebSocket support in both
