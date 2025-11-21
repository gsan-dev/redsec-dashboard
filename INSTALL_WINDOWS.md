# Installation Guide - Windows

This guide covers installing RedSec Dashboard on Windows 10/11.

## Prerequisites

- Windows 10/11
- Administrator access
- Internet connection

## Step 1: Install Nmap

### Option 1: Direct Download (Recommended)

1. Go to [nmap.org/download.html](https://nmap.org/download.html)
2. Download "Latest stable release self-installer" for Windows
3. Run the installer
4. **IMPORTANT:** Check "Add Nmap to System PATH" during installation
5. Complete the installation

### Option 2: Using winget

```powershell
winget install Insecure.Nmap
```

### Option 3: Using Chocolatey

```powershell
choco install nmap -y
```

### Verify Installation

Open a new PowerShell window:
```powershell
nmap --version
```

## Step 2: Install Python 3.11+

### Option 1: Direct Download

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.11 or newer
3. Run installer
4. **IMPORTANT:** Check "Add Python to PATH"
5. Click "Install Now"

### Option 2: Using winget

```powershell
winget install Python.Python.3.11
```

### Verify Installation

```powershell
python --version
pip --version
```

## Step 3: Install Node.js

### Option 1: Direct Download

1. Go to [nodejs.org](https://nodejs.org/)
2. Download LTS version
3. Run installer with default options

### Option 2: Using winget

```powershell
winget install OpenJS.NodeJS.LTS
```

### Verify Installation

```powershell
node --version
npm --version
```

## Step 4: Install Git (Optional)

Only needed if cloning from GitHub:

```powershell
winget install Git.Git
```

## Step 5: Get RedSec Dashboard

### Option 1: Clone from GitHub

```powershell
git clone https://github.com/yourusername/redsec-dashboard.git
cd redsec-dashboard
```

### Option 2: Download ZIP

1. Download ZIP from GitHub
2. Extract to your preferred location
3. Open PowerShell in that directory

## Step 6: Setup Backend

```powershell
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

You should see:
```
Successfully installed fastapi uvicorn ...
```

## Step 7: Setup Frontend

```powershell
cd ..\frontend

# Install dependencies
npm install
```

This may take a few minutes...

## Step 8: Test the Installation

### Start Backend

Open PowerShell in `backend` directory:

```powershell
.\venv\Scripts\activate
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
🚀 Starting RedSec Dashboard...
✅ Loaded 1 plugin(s)
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Start Frontend

Open a **second PowerShell** in `frontend` directory:

```powershell
npm run dev
```

You should see:
```
VITE ready in XXX ms
➜  Local:   http://localhost:5173/
```

## Step 9: Access the Dashboard

Open your browser and navigate to:
- **Dashboard:** http://localhost:5173
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Using the Startup Script

For easier startup, use the provided script:

```powershell
.\start.ps1
```

This will automatically:
- Open two PowerShell windows
- Start backend and frontend
- Display URLs

To stop: Close the PowerShell windows or press Ctrl+C

## Running with Administrator Privileges (For OS Detection)

For accurate OS detection, run PowerShell as Administrator:

1. Right-click PowerShell → "Run as Administrator"
2. Navigate to backend directory
3. Run:
```powershell
cd C:\path\to\redsec-dashboard\backend
.\venv\Scripts\activate
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Using Docker (Alternative)

If you have Docker Desktop:

```powershell
# Install Docker Desktop from docker.com

# Start RedSec
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Troubleshooting

### "nmap: command not found"

- Nmap not in PATH
- Restart PowerShell after installing
- Reinstall Nmap and check "Add to PATH"

### "python: command not found"

- Python not in PATH
- Restart PowerShell
- Reinstall Python and check "Add Python to PATH"

### Port Already in Use

```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

### Virtual Environment Not Activating

```powershell
# Enable script execution (run as Admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Module Import Errors

```powershell
# Reinstall dependencies
cd backend
.\venv\Scripts\activate
pip install --upgrade -r requirements.txt
```

### Frontend Won't Start

```powershell
# Clear and reinstall
cd frontend
Remove-Item node_modules -Recurse -Force
Remove-Item package-lock.json
npm install
```

## Windows Firewall

If you can't access from other devices on your network:

1. Open Windows Defender Firewall
2. Click "Advanced settings"
3. Create **Inbound Rules** for:
   - Port 8000 (Backend)
   - Port 5173 (Frontend)

Or use PowerShell as Admin:
```powershell
# Allow backend port
netsh advfirewall firewall add rule name="RedSec Backend" dir=in action=allow protocol=TCP localport=8000

# Allow frontend port
netsh advfirewall firewall add rule name="RedSec Frontend" dir=in action=allow protocol=TCP localport=5173
```

## Production Deployment

For production on Windows Server:

1. Use IIS as reverse proxy
2. Run backend as Windows Service
3. Use production build of frontend

See the main [README.md](../README.md) for more details.

## Next Steps

1. Configure environment variables (`.env`)
2. Review security settings
3. Set up regular backups
4. Explore the dashboard features

For more information, see the main [README.md](../README.md) and [Documentation](../docs/).
