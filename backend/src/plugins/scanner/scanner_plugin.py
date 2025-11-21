"""
Scanner Plugin - Network device discovery and monitoring
"""
import asyncio
import socket
import netifaces
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import platform
import subprocess
import re


class Device:
    """Represents a network device"""
    def __init__(self, ip: str, mac: str = "", hostname: str = "", 
                 vendor: str = "", status: str = "active"):
        self.ip = ip
        self.mac = mac
        self.hostname = hostname
        self.vendor = vendor
        self.status = status
        self.first_seen = datetime.now()
        self.last_seen = datetime.now()
        self.ports = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "ip": self.ip,
            "mac": self.mac,
            "hostname": self.hostname,
            "vendor": self.vendor,
            "status": self.status,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "ports": self.ports
        }


class ScannerPlugin(BasePlugin):
    """Network Scanner Plugin"""
    
    def __init__(self, plugin_dir: Path):
        super().__init__(plugin_dir)
        self.devices: Dict[str, Device] = {}
        self.is_scanning = False
        
    async def initialize(self) -> bool:
        """Initialize the scanner plugin"""
        try:
            # Test if we can get network interfaces
            interfaces = netifaces.interfaces()
            if not interfaces:
                return False
            return True
        except Exception as e:
            print(f"Scanner initialization failed: {e}")
            return False
    
    def _get_default_gateway_and_subnet(self) -> tuple[Optional[str], Optional[str]]:
        """Get the default gateway and subnet"""
        try:
            gws = netifaces.gateways()
            default_gw = gws['default'][netifaces.AF_INET]
            interface = default_gw[1]
            
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                addr_info = addrs[netifaces.AF_INET][0]
                ip = addr_info['addr']
                netmask = addr_info.get('netmask', '255.255.255.0')
                
                # Calculate network range
                ip_parts = ip.split('.')
                netmask_parts = netmask.split('.')
                
                network = '.'.join([
                    str(int(ip_parts[i]) & int(netmask_parts[i])) 
                    for i in range(4)
                ])
                
                return default_gw[0], network
        except Exception as e:
            print(f"Error getting network info: {e}")
        
        return None, None
    
    async def _ping_host(self, ip: str) -> bool:
        """Ping a host to check if it's alive"""
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
            # Increased timeout to 2000ms for Windows, 2s for Linux
            timeout_value = '2000' if platform.system().lower() == 'windows' else '2'
            command = ['ping', param, '1', timeout_param, timeout_value, ip]
            
            result = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await result.communicate()
            
            # Debug: Print first successful ping
            if result.returncode == 0 and ip.endswith('.1'):
                print(f"✅ Successfully pinged {ip}")
            
            return result.returncode == 0
        except Exception as e:
            # Only print error for gateway IP
            if ip.endswith('.1'):
                print(f"❌ Error pinging {ip}: {e}")
            return False
    
    async def _get_hostname(self, ip: str) -> str:
        """Try to get hostname for an IP"""
        try:
            hostname = await asyncio.to_thread(socket.gethostbyaddr, ip)
            return hostname[0]
        except:
            return ""
    
    async def _get_mac_address(self, ip: str) -> str:
        """Get MAC address for an IP (platform dependent)"""
        try:
            if platform.system().lower() == 'windows':
                result = await asyncio.create_subprocess_exec(
                    'arp', '-a', ip,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, _ = await result.communicate()
                output = stdout.decode()
                
                # Parse ARP output
                mac_pattern = r'([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})'
                match = re.search(mac_pattern, output)
                if match:
                    return match.group(0).replace('-', ':').upper()
            else:
                # Linux/Mac
                result = await asyncio.create_subprocess_exec(
                    'arp', '-n', ip,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, _ = await result.communicate()
                output = stdout.decode()
                
                mac_pattern = r'([0-9a-fA-F]{2}:){5}([0-9a-fA-F]{2})'
                match = re.search(mac_pattern, output)
                if match:
                    return match.group(0).upper()
        except Exception as e:
            print(f"Error getting MAC for {ip}: {e}")
        
        return ""
    
    def _get_vendor_from_mac(self, mac: str) -> str:
        """Get vendor name from MAC address (OUI lookup)"""
        # This is a simplified version. In production, use an OUI database
        oui_db = {
            "00:50:56": "VMware",
            "08:00:27": "VirtualBox",
            "52:54:00": "QEMU/KVM",
            "00:1B:63": "Apple",
            "00:25:00": "Apple",
            "DC:A6:32": "Raspberry Pi",
            "B8:27:EB": "Raspberry Pi",
        }
        
        if mac:
            oui = mac[:8].upper()
            return oui_db.get(oui, "Unknown")
        return ""
    
    async def _scan_device(self, ip: str) -> Optional[Device]:
        """Scan a single device"""
        if await self._ping_host(ip):
            hostname = await self._get_hostname(ip)
            mac = await self._get_mac_address(ip)
            vendor = self._get_vendor_from_mac(mac)
            
            device = Device(
                ip=ip,
                mac=mac,
                hostname=hostname,
                vendor=vendor,
                status="active"
            )
            return device
        return None
    
    async def scan_network(self, network_range: Optional[str] = None) -> List[Dict[str, Any]]:
        """Scan the network for devices using nmap"""
        if self.is_scanning:
            return [d.to_dict() for d in self.devices.values()]
        
        self.is_scanning = True
        discovered_devices = []
        
        try:
            # Import nmap
            import nmap
            
            # Get network range if not provided
            if not network_range:
                print("🔍 Detecting network configuration...")
                gateway, subnet = self._get_default_gateway_and_subnet()
                print(f"   Gateway: {gateway}")
                print(f"   Subnet: {subnet}")
                
                if not subnet:
                    print("❌ Could not detect network subnet")
                    return []
                
                # Generate network range in CIDR notation
                base_ip = '.'.join(subnet.split('.')[:3])
                network_range = f"{base_ip}.0/24"
                print(f"📡 Scanning network: {network_range}")
            
            # Initialize nmap scanner
            nm = nmap.PortScanner()
            
            print(f"🚀 Starting nmap scan (this may take 30-60 seconds)...")
            
            # Determine scan arguments based on privileges and OS
            scan_args = '-sn'  # Basic ping scan (no OS detection)
            os_detection_enabled = False
            
            # Try to detect if we have necessary privileges for advanced scanning
            try:
                # Test nmap capabilities with a quick scan on localhost
                test_nm = nmap.PortScanner()
                test_nm.scan('127.0.0.1', arguments='-sS -p 80', sudo=False)
                # If we get here, we have privileges for SYN scan
                # For OS detection, we need port scan + OS detection
                # -sS: SYN scan (requires privileges but faster than full connect)
                # -O: OS detection
                # -F: Fast scan (top 100 ports instead of 1000)
                # --osscan-guess: Guess OS more aggressively
                scan_args = '-sS -F -O --osscan-guess'
                os_detection_enabled = True
                print(f"   ✅ Running with OS detection enabled (SYN scan)")
                print(f"   ⏱️  This will take longer (scanning ports + OS detection)")
            except Exception:
                # No privileges for SYN scan, use simple ping scan
                print(f"   ℹ️  Running basic network scan (ping + ARP)")
                if platform.system().lower() == 'windows':
                    print(f"   💡 For OS detection: Run as Administrator + allow firewall")
                else:
                    print(f"   💡 For OS detection: Run with sudo")
            
            # Perform the actual scan
            try:
                await asyncio.to_thread(
                    nm.scan,
                    hosts=network_range,
                    arguments=scan_args
                )
            except Exception as e:
                print(f"   ❌ Scan error: {str(e)[:100]}...")
                # Try fallback to basic ping scan
                print(f"   🔄 Retrying with basic scan...")
                scan_args = '-sn'
                os_detection_enabled = False
                await asyncio.to_thread(
                    nm.scan,
                    hosts=network_range,
                    arguments=scan_args
                )
            
            # Process results
            device_count = 0
            for host in nm.all_hosts():
                if nm[host].state() == 'up':
                    hostname = nm[host].hostname() if nm[host].hostname() else ""
                    
                    # Get MAC address and vendor
                    mac = ""
                    vendor = ""
                    if 'mac' in nm[host]['addresses']:
                        mac = nm[host]['addresses']['mac']
                        if 'vendor' in nm[host] and nm[host]['vendor']:
                            vendor = list(nm[host]['vendor'].values())[0] if nm[host]['vendor'] else ""
                    
                    # Get OS information if available
                    os_info = ""
                    if 'osmatch' in nm[host] and nm[host]['osmatch']:
                        os_match = nm[host]['osmatch'][0]
                        os_info = os_match.get('name', '')
                    
                    # Get open ports if any were scanned
                    ports = []
                    if 'tcp' in nm[host]:
                        ports = [port for port in nm[host]['tcp'].keys()]
                    
                    # Create device object
                    device = Device(
                        ip=host,
                        mac=mac,
                        hostname=hostname,
                        vendor=vendor,
                        status="active"
                    )
                    device.ports = ports
                    if os_info:
                        device.os_info = os_info
                    
                    self.devices[host] = device
                    device_dict = device.to_dict()
                    if os_info:
                        device_dict['os_info'] = os_info
                    discovered_devices.append(device_dict)
                    device_count += 1
                    
                    print(f"   ✅ Found: {host} ({hostname or 'Unknown'}) - {vendor or 'Unknown vendor'}")
            
            print(f"✅ Scan complete! Found {device_count} device(s)")
        
        except ImportError:
            print("❌ Error: python-nmap not installed. Run: pip install python-nmap")
        except Exception as e:
            print(f"❌ Error during scan: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_scanning = False
        
        return discovered_devices
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute scan operation"""
        action = kwargs.get('action', 'scan')
        
        if action == 'scan':
            network = kwargs.get('network', None)
            devices = await self.scan_network(network)
            return {
                "status": "success",
                "action": "scan",
                "devices": devices,
                "total": len(devices)
            }
        
        elif action == 'list':
            return {
                "status": "success",
                "action": "list",
                "devices": [d.to_dict() for d in self.devices.values()],
                "total": len(self.devices)
            }
        
        elif action == 'get_device':
            ip = kwargs.get('ip')
            device = self.devices.get(ip)
            if device:
                return {
                    "status": "success",
                    "device": device.to_dict()
                }
            return {
                "status": "error",
                "message": f"Device {ip} not found"
            }
        
        return {
            "status": "error",
            "message": f"Unknown action: {action}"
        }
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        self.devices.clear()
        self.is_scanning = False
