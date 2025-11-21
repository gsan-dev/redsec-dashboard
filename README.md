<div align="center">

# 🛡️ RedSec Dashboard

### Advanced Network Security & Monitoring Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

**A modular, open-source network monitoring solution for homelabs, SMBs, and security professionals**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

<img src="docs/images/dashboard-preview.png" alt="RedSec Dashboard" width="800"/>

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
  - [Windows](#windows)
  - [Linux](#linux)
  - [Docker](#docker)
- [Usage](#-usage)
- [Plugin System](#-plugin-system)
- [Configuration](#-configuration)
- [Development](#-development)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

**RedSec Dashboard** is a professional-grade network security and monitoring platform designed for homelabs, small-to-medium businesses, and security enthusiasts. Built with a modular plugin architecture, it provides real-time network visibility, device discovery, and extensible monitoring capabilities.

### Why RedSec?

- 🔌 **Modular Plugin System** - Extend functionality with custom plugins
- 🚀 **Easy Deployment** - Docker-ready with one-command setup
- 🎨 **Modern UI** - Beautiful, responsive dark-themed interface
- 🔒 **Security-First** - Built by security professionals, for security professionals
- 💻 **Cross-Platform** - Works on Windows, Linux, and macOS
- 📊 **Real-Time Monitoring** - Live network activity and device tracking

## ✨ Features

### Core Features

- **🔍 Network Scanner**
  - Automatic device discovery using nmap
  - Real-time network mapping
  - MAC address identification
  - Vendor detection (OUI database)
  - OS fingerprinting (with admin privileges)
  - Port scanning capabilities

- **🔌 Plugin System**
  - Hot-loadable plugins
  - Easy plugin development
  - Isolated plugin environments
  - Plugin marketplace (coming soon)

- **📊 Dashboard**
  - Real-time statistics
  - Device inventory
  - Network topology visualization
  - Historical data tracking

- **🎨 Modern Interface**
  - Responsive design
  - Dark theme optimized
  - Intuitive navigation
  - Real-time updates

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│         Frontend (React + TypeScript)           │
│  • Modern Dashboard UI                          │
│  • Network Visualization                        │
│  • Plugin Management Interface                  │
└──────────────────┬──────────────────────────────┘
                   │ REST API
┌──────────────────┴──────────────────────────────┐
│          Backend (Python + FastAPI)             │
│  ┌────────────────────────────────────────────┐ │
│  │         Plugin Manager (Core)              │ │
│  └────────────┬───────────────────────────────┘ │
│               │                                  │
│  ┌────────────┴─────────┬──────────────┐       │
│  │  Scanner Plugin      │ Future Plugins│       │
│  │  • Device Discovery  │ • Firewall    │       │
│  │  • Network Mapping   │ • Bandwidth   │       │
│  │  • Port Scanning     │ • IDS/IPS     │       │
│  └──────────────────────┴──────────────┘       │
└─────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Python 3.11+
- FastAPI - High-performance async web framework
- SQLAlchemy - Database ORM
- Nmap - Network scanning engine
- Pydantic - Data validation

**Frontend:**
- React 18 with TypeScript
- Vite - Next-generation build tool
- Modern CSS with custom design system

**Infrastructure:**
- Docker & Docker Compose
- SQLite (development) / PostgreSQL (production ready)

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Nmap** ([Download](https://nmap.org/download.html))
- **Docker** (optional, for containerized deployment)

### Quick Installation

#### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/redsec-dashboard.git
cd redsec-dashboard

# Start with Docker Compose
docker-compose up -d

# Access the dashboard
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
```

#### Manual Setup

**Windows:**
```powershell
# Clone and navigate
git clone https://github.com/yourusername/redsec-dashboard.git
cd redsec-dashboard

# Run startup script
.\start.ps1
```

**Linux:**
```bash
# Clone and navigate
git clone https://github.com/yourusername/redsec-dashboard.git
cd redsec-dashboard

# Run startup script
chmod +x start.sh
./start.sh
```

## 📦 Installation

### Windows

#### 1. Install Prerequisites

**Nmap:**
- Download from [nmap.org](https://nmap.org/download.html)
- Run installer and check "Add to PATH"

**Python & Node.js:**
```powershell
# Using winget
winget install Python.Python.3.11
winget install OpenJS.NodeJS

# Or download from official websites
```

#### 2. Setup Backend

```powershell
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Setup Frontend

```powershell
cd frontend

# Install dependencies
npm install
```

#### 4. Run the Application

**Option 1 - Using the script:**
```powershell
.\start.ps1
```

**Option 2 - Manual:**
```powershell
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Linux

#### 1. Install Prerequisites

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3.11 python3-pip nodejs npm nmap

# Fedora/RHEL
sudo dnf install -y python3.11 python3-pip nodejs npm nmap

# Arch Linux
sudo pacman -S python nodejs npm nmap
```

#### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install
```

#### 4. Run the Application

**Option 1 - Using the script:**
```bash
chmod +x start.sh
./start.sh
```

**Option 2 - Manual:**
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 💻 Usage

### Accessing the Dashboard

Once running, access the dashboard at:

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

### Running Network Scans

1. Navigate to **Network Scanner** in the sidebar
2. Click **Start Scan**
3. Wait 30-60 seconds for scan completion
4. View discovered devices in the grid

### OS Detection (Advanced)

For accurate OS detection, run with elevated privileges:

**Windows:**
```powershell
# Run PowerShell as Administrator
cd backend
.\venv\Scripts\activate
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Linux:**
```bash
# Run with sudo
cd backend
source venv/bin/activate
sudo venv/bin/python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔌 Plugin System

RedSec Dashboard features a powerful plugin architecture for extending functionality.

### Creating a Plugin

1. Create plugin directory: `backend/src/plugins/your-plugin/`
2. Add `plugin.json`:

```json
{
  "name": "your-plugin",
  "version": "1.0.0",
  "description": "Your plugin description",
  "endpoints": ["/api/your-endpoint"],
  "ui_component": "YourComponent"
}
```

3. Create `your-plugin_plugin.py`:

```python
from core.plugin_base import BasePlugin

class YourPlugin(BasePlugin):
    async def initialize(self) -> bool:
        return True
    
    async def execute(self, **kwargs):
        return {"status": "success"}
    
    async def cleanup(self) -> None:
        pass
```

See [Plugin Development Guide](docs/PLUGIN_DEVELOPMENT.md) for details.

## ⚙️ Configuration

### Environment Variables

Create `.env` file in `backend/`:

```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
DATABASE_URL=sqlite:///./redsec.db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:5173
```

### Database Configuration

Default: SQLite (development)  
Production: PostgreSQL recommended

Update `DATABASE_URL` in `.env` for PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/redsec
```

## 🛠️ Development

### Project Structure

```
redsec-dashboard/
├── backend/
│   ├── src/
│   │   ├── core/          # Plugin system core
│   │   ├── plugins/       # Plugin implementations
│   │   ├── api/           # API routes
│   │   └── main.py        # FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── App.tsx
│   │   └── index.css
│   ├── package.json
│   └── Dockerfile
├── docs/                  # Documentation
├── docker-compose.yml
└── README.md
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Style

**Backend:**
- Follow PEP 8
- Use type hints
- Document with docstrings

**Frontend:**
- ESLint configuration provided
- TypeScript strict mode
- React best practices

## 🗺️ Roadmap

### Version 1.1 (Q1 2025)
- [ ] Database persistence
- [ ] WebSocket support for real-time updates
- [ ] User authentication system
- [ ] Enhanced device fingerprinting

### Version 1.2 (Q2 2025)
- [ ] Bandwidth monitoring plugin
- [ ] Port scanner plugin
- [ ] Alert system for new devices
- [ ] Network topology visualization (D3.js)

### Version 2.0 (Q3 2025)
- [ ] Plugin marketplace
- [ ] Multi-user support
- [ ] REST API v2
- [ ] Mobile app (React Native)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/redsec-dashboard.git
cd redsec-dashboard

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Create a branch
git checkout -b feature/my-feature
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Nmap Project](https://nmap.org/) - Network scanning engine
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [React](https://reactjs.org/) - UI library
- The open-source community

## 📮 Contact & Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/yourusername/redsec-dashboard/issues)
- **Discussions:** [Join the community](https://github.com/yourusername/redsec-dashboard/discussions)
- **Email:** your.email@example.com

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by the RedSec Team

[Report Bug](https://github.com/yourusername/redsec-dashboard/issues) • [Request Feature](https://github.com/yourusername/redsec-dashboard/issues) • [Documentation](docs/)

</div>
