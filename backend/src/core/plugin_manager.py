"""
Plugin Manager - Handles loading, registration and execution of plugins
"""
import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Optional, Type, Any
from .plugin_base import BasePlugin
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PluginManager:
    """Manages all plugins in the system"""
    
    def __init__(self, plugins_dir: Path):
        self.plugins_dir = plugins_dir
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugin_classes: Dict[str, Type[BasePlugin]] = {}
        
    async def discover_plugins(self) -> List[str]:
        """Discover all available plugins in the plugins directory"""
        discovered = []
        
        if not self.plugins_dir.exists():
            logger.warning(f"Plugins directory not found: {self.plugins_dir}")
            return discovered
        
        for plugin_path in self.plugins_dir.iterdir():
            if plugin_path.is_dir() and (plugin_path / "plugin.json").exists():
                plugin_name = plugin_path.name
                discovered.append(plugin_name)
                logger.info(f"Discovered plugin: {plugin_name}")
        
        return discovered
    
    def _load_plugin_class(self, plugin_name: str) -> Optional[Type[BasePlugin]]:
        """Dynamically load a plugin class from its module"""
        plugin_path = self.plugins_dir / plugin_name
        module_file = plugin_path / f"{plugin_name}_plugin.py"
        
        if not module_file.exists():
            logger.error(f"Plugin module not found: {module_file}")
            return None
        
        try:
            # Add src directory to path to enable imports
            src_dir = self.plugins_dir.parent
            if str(src_dir) not in sys.path:
                sys.path.insert(0, str(src_dir))
            
            # Read and execute the plugin file
            with open(module_file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Import necessary modules for the plugin
            import asyncio
            import socket
            import netifaces
            from datetime import datetime
            import platform
            import subprocess
            import re
            
            # Create a namespace for the plugin with all necessary imports
            namespace = {
                '__file__': str(module_file),
                '__name__': f"plugins.{plugin_name}",
                '__builtins__': __builtins__,
                'asyncio': asyncio,
                'socket': socket,
                'netifaces': netifaces,
                'Path': Path,
                'Dict': Dict,
                'Any': Any,
                'List': List,
                'Optional': Optional,
                'datetime': datetime,
                'platform': platform,
                'subprocess': subprocess,
                're': re,
                'BasePlugin': BasePlugin,
            }
            
            # Execute the plugin code
            exec(code, namespace)
            
            # Look for a class that inherits from BasePlugin
            for name, obj in namespace.items():
                if (isinstance(obj, type) and 
                    issubclass(obj, BasePlugin) and 
                    obj is not BasePlugin):
                    logger.info(f"Found plugin class: {name}")
                    return obj
            
            logger.error(f"No valid plugin class found in {module_file}")
            return None
            
        except Exception as e:
            logger.error(f"Error loading plugin {plugin_name}: {e}", exc_info=True)
            return None
    
    async def load_plugin(self, plugin_name: str) -> bool:
        """Load and initialize a specific plugin"""
        if plugin_name in self.plugins:
            logger.warning(f"Plugin {plugin_name} already loaded")
            return True
        
        plugin_class = self._load_plugin_class(plugin_name)
        if not plugin_class:
            return False
        
        try:
            plugin_path = self.plugins_dir / plugin_name
            plugin_instance = plugin_class(plugin_path)
            
            # Initialize the plugin
            if await plugin_instance.initialize():
                self.plugins[plugin_name] = plugin_instance
                self.plugin_classes[plugin_name] = plugin_class
                logger.info(f"Successfully loaded plugin: {plugin_name}")
                return True
            else:
                logger.error(f"Plugin {plugin_name} initialization failed")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing plugin {plugin_name}: {e}")
            return False
    
    async def load_all_plugins(self) -> None:
        """Discover and load all available plugins"""
        discovered = await self.discover_plugins()
        for plugin_name in discovered:
            await self.load_plugin(plugin_name)
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """Get a loaded plugin by name"""
        return self.plugins.get(plugin_name)
    
    def list_plugins(self) -> List[Dict]:
        """List all loaded plugins with their metadata"""
        return [
            {
                "name": name,
                "metadata": plugin.get_metadata()
            }
            for name, plugin in self.plugins.items()
        ]
    
    async def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin and cleanup its resources"""
        plugin = self.plugins.get(plugin_name)
        if not plugin:
            logger.warning(f"Plugin {plugin_name} not loaded")
            return False
        
        try:
            await plugin.cleanup()
            del self.plugins[plugin_name]
            logger.info(f"Unloaded plugin: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Error unloading plugin {plugin_name}: {e}")
            return False
