# Installation Guide - Linux (Ubuntu Server 24.04 LTS)

This guide covers installing RedSec Dashboard on Ubuntu Server 24.04 LTS. The process is similar for other Linux distributions with minor package manager differences.

## Prerequisites

- Ubuntu Server 24.04 LTS (or similar Linux distribution)
- Sudo/root access
- Internet connection

## Step 1: Update System

```bash
sudo apt update && sudo apt upgrade -y
```

## Step 2: Install Required Dependencies

### Install Python 3.11+

```bash
# Ubuntu 24.04 comes with Python 3.12 by default
sudo apt install -y python3 python3-pip python3-venv
```

### Install Node.js and npm

```bash
# Using NodeSource repository for latest LTS
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node --version
npm --version
```

### Install Nmap

```bash
sudo apt install -y nmap

# Verify installation
nmap --version
```

### Install Git

```bash
sudo apt install -y git
```

## Step 3: Clone the Repository

```bash
# Clone to your preferred location
cd /opt  # or ~/projects, etc.
git clone https://github.com/yourusername/redsec-dashboard.git
cd redsec-dashboard
```

## Step 4: Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi; print('FastAPI installed successfully')"
```

## Step 5: Setup Frontend

```bash
cd ../frontend

# Install Node.js dependencies
npm install

# This may take a few minutes...
```

## Step 6: Configure Environment (Optional)

```bash
cd ../backend

# Copy example environment file
cp .env.example .env

# Edit configuration if needed
nano .env
```

## Step 7: Test the Installation

### Start Backend

```bash
cd backend
source venv/bin/activate
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
🚀 Starting RedSec Dashboard...
✅ Loaded 1 plugin(s)
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Start Frontend (in another terminal)

```bash
cd frontend
npm run dev
```

You should see:
```
VITE ready in XXX ms
➜  Local:   http://localhost:5173/
```

## Step 8: Access the Dashboard

Open your browser and navigate to:
- **Dashboard:** http://your-server-ip:5173
- **API:** http://your-server-ip:8000
- **API Docs:** http://your-server-ip:8000/docs

## Running with Privileges (For OS Detection)

To enable OS detection, run backend with sudo:

```bash
cd backend
source venv/bin/activate
sudo venv/bin/python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Step 9: Setup as SystemD Service (Production)

For production deployments, set up as a system service:

### Create Backend Service

```bash
sudo nano /etc/systemd/system/redsec-backend.service
```

Add:
```ini
[Unit]
Description=RedSec Dashboard Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/redsec-dashboard/backend
Environment="PATH=/opt/redsec-dashboard/backend/venv/bin"
ExecStart=/opt/redsec-dashboard/backend/venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Create Frontend Service

```bash
sudo nano /etc/systemd/system/redsec-frontend.service
```

Add:
```ini
[Unit]
Description=RedSec Dashboard Frontend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/redsec-dashboard/frontend
ExecStart=/usr/bin/npm run dev
Restart=always

[Install]
WantedBy=multi-user.target
```

### Enable and Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable redsec-backend
sudo systemctl enable redsec-frontend

# Start services
sudo systemctl start redsec-backend
sudo systemctl start redsec-frontend

# Check status
sudo systemctl status redsec-backend
sudo systemctl status redsec-frontend
```

## Using the Startup Script

For development, use the provided startup script:

```bash
chmod +x start.sh
./start.sh
```

This will start both backend and frontend automatically.

## Firewall Configuration

If you're using UFW (Ubuntu Firewall):

```bash
# Allow ports
sudo ufw allow 8000/tcp  # Backend API
sudo ufw allow 5173/tcp  # Frontend (dev server)

# For production with reverse proxy
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

## Using Docker (Alternative)

For a simpler deployment, use Docker:

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install -y docker-compose

# Start RedSec
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
sudo lsof -i :8000
sudo lsof -i :5173

# Kill the process
sudo kill -9 <PID>
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R $USER:$USER /opt/redsec-dashboard

# Fix permissions
chmod +x start.sh
```

### Nmap Not Finding Devices

```bash
# Run with sudo
sudo venv/bin/python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or add capabilities (persistent)
sudo setcap cap_net_raw,cap_net_admin=eip $(which nmap)
```

### Frontend Build Errors

```bash
# Clear node modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Production Deployment with Nginx

### Install Nginx

```bash
sudo apt install -y nginx
```

### Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/redsec
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/redsec /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Next Steps

1. Change default passwords and API keys
2. Configure SSL/TLS with Let's Encrypt
3. Set up regular backups
4. Configure monitoring
5. Review security best practices

For more information, see the main [README.md](../README.md) and [Documentation](../docs/).
