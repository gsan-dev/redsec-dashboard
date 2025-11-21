"""
Base Plugin System for RedSec Dashboard
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import json
from pathlib import Path


class PluginMetadata(BaseModel):
    """Plugin metadata model"""
    name: str
    version: str
    description: str
    author: Optional[str] = "Unknown"
    endpoints: List[str] = []
    ui_component: Optional[str] = None
    enabled: bool = True


class BasePlugin(ABC):
    """Abstract base class for all plugins"""
    
    def __init__(self, plugin_dir: Path):
        self.plugin_dir = plugin_dir
        self.metadata = self._load_metadata()
        
    def _load_metadata(self) -> PluginMetadata:
        """Load plugin metadata from plugin.json"""
        metadata_file = self.plugin_dir / "plugin.json"
        if not metadata_file.exists():
            raise FileNotFoundError(f"plugin.json not found in {self.plugin_dir}")
        
        with open(metadata_file, 'r') as f:
            data = json.load(f)
        
        return PluginMetadata(**data)
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the plugin. Return True if successful."""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the main plugin functionality"""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup resources when plugin is disabled"""
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return plugin metadata"""
        return self.metadata.model_dump()
