"""
API Routes for RedSec Dashboard
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

router = APIRouter()

# Will be injected by main.py
plugin_manager = None


class ScanRequest(BaseModel):
    network: Optional[str] = None


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RedSec Dashboard API"}


@router.get("/plugins")
async def list_plugins():
    """List all available plugins"""
    if not plugin_manager:
        raise HTTPException(status_code=500, detail="Plugin manager not initialized")
    
    return {
        "plugins": plugin_manager.list_plugins()
    }


@router.post("/scan")
async def start_scan(request: ScanRequest):
    """Start a network scan"""
    if not plugin_manager:
        raise HTTPException(status_code=500, detail="Plugin manager not initialized")
    
    scanner = plugin_manager.get_plugin("scanner")
    if not scanner:
        raise HTTPException(status_code=404, detail="Scanner plugin not found")
    
    result = await scanner.execute(action='scan', network=request.network)
    return result


@router.get("/devices")
async def get_devices():
    """Get all discovered devices"""
    if not plugin_manager:
        raise HTTPException(status_code=500, detail="Plugin manager not initialized")
    
    scanner = plugin_manager.get_plugin("scanner")
    if not scanner:
        raise HTTPException(status_code=404, detail="Scanner plugin not found")
    
    result = await scanner.execute(action='list')
    return result


@router.get("/device/{ip}")
async def get_device(ip: str):
    """Get specific device information"""
    if not plugin_manager:
        raise HTTPException(status_code=500, detail="Plugin manager not initialized")
    
    scanner = plugin_manager.get_plugin("scanner")
    if not scanner:
        raise HTTPException(status_code=404, detail="Scanner plugin not found")
    
    result = await scanner.execute(action='get_device', ip=ip)
    
    if result.get('status') == 'error':
        raise HTTPException(status_code=404, detail=result.get('message'))
    
    return result
