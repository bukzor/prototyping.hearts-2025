# Web Framework

HTTP server, routing, WebSocket support.

| | POC | Production |
|-|-----|------------|
| Framework | FastAPI | axum |
| Runtime | uvicorn | tokio |

## Notes

- Both async-first
- axum is tower-based, composes middleware similarly
- FastAPI's automatic OpenAPI docs don't have direct axum equivalent
- WebSocket support in both
