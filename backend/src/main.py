"""
RedSec Dashboard - Main FastAPI Application
"""
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .core.plugin_manager import PluginManager
from .api import routes

# Initialize FastAPI app
app = FastAPI(
    title="RedSec Dashboard API",
    description="Network monitoring and security dashboard with plugin system",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize plugin manager
BASE_DIR = Path(__file__).parent
PLUGINS_DIR = BASE_DIR / "plugins"
plugin_manager = PluginManager(PLUGINS_DIR)

# Inject plugin manager into routes
routes.plugin_manager = plugin_manager

# Include API routes
app.include_router(routes.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Initialize plugins on startup"""
    print("🚀 Starting RedSec Dashboard...")
    await plugin_manager.load_all_plugins()
    print(f"✅ Loaded {len(plugin_manager.plugins)} plugin(s)")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down RedSec Dashboard...")
    for plugin_name in list(plugin_manager.plugins.keys()):
        await plugin_manager.unload_plugin(plugin_name)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RedSec Dashboard API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
