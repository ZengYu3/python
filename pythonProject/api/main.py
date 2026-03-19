from fastapi import FastAPI
from api.routes import sessions, messages, health
from api.websocket import router as ws_router

app = FastAPI(title="Computer Use Product API")

# Include HTTP REST endpoints
app.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
app.include_router(health.router, prefix="/health", tags=["Health"])

# Include WebSocket endpoint
app.include_router(ws_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Computer Use Product API is running."}