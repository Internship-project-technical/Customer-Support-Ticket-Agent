from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models

from .routers import auth, tickets, agents, faq

app = FastAPI(
    title="AI Customer Support Ticket System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 🔥 CREATE TABLES AUTOMATICALLY
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(agents.router)
app.include_router(faq.router)

@app.get("/")
async def root():
    return {
        "message": "AI Customer Support Ticket System API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/auth",
            "tickets": "/tickets",
            "agents": "/agents",
            "faq": "/faq"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "running"}