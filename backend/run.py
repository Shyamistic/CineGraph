import uvicorn

from app.config import settings

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.cinegraph_host, port=settings.cinegraph_port, reload=True)
