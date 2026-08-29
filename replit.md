# Watch Buddy on Replit

## Run

The `Start application` workflow runs both services:

- FastAPI backend on port `8000`
- Vite frontend on port `5000`

Manual command:

```bash
bash start.sh
```

Install frontend dependencies with `npm ci --prefix frontend` if `frontend/node_modules` is missing.

The app remains usable in clearly labeled demo mode without external credentials. Gemini/Vertex, ClickHouse, and OTLP capabilities appear as live only when their corresponding environment configuration is available.