# RedSec Dashboard - Docker Quick Start

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## One-Command Deployment

```bash
# Clone the repository
git clone https://github.com/yourusername/redsec-dashboard.git
cd redsec-dashboard

# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## What It Does Automatically

The Docker setup will automatically:

✅ Install Python 3.11 and all dependencies  
✅ Install Node.js 20 and npm packages  
✅ Install nmap and network tools  
✅ Configure network capabilities for scanning  
✅ Set up proper networking between services  
✅ Enable health checks  
✅ Set up volume mounts for development  
✅ Configure auto-restart  

## Useful Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build

# Stop and remove everything (including volumes)
docker-compose down -v

# Check service status
docker-compose ps

# Execute command in running container
docker-compose exec backend python -c "print('Hello')"
docker-compose exec frontend npm list
```

## Network Scanning

The backend container runs in **privileged mode** with network capabilities:
- `CAP_NET_ADMIN` - Network administration
- `CAP_NET_RAW` - Raw socket access
- `CAP_SYS_ADMIN` - System administration

This allows nmap to:
- Perform SYN scans
- Detect operating systems
- Access network interfaces
- Perform ARP scans

## Development Mode

The Docker setup is configured for development:

- **Hot reload enabled** for both frontend and backend
- **Source mounted as volumes** - changes reflect immediately
- **Debug mode enabled** - detailed error messages
- **Port forwarding** - direct access from host machine

## Troubleshooting

### Port already in use

```bash
# Check what's using the port
sudo lsof -i :8000
sudo lsof -i :5173

# Or change ports in docker-compose.yml
ports:
  - "8001:8000"  # Backend on 8001
  - "3000:5173"  # Frontend on 3000
```

### Backend not starting

```bash
# Check logs
docker-compose logs backend

# Rebuild
docker-compose up -d --build backend

# Enter container
docker-compose exec backend /bin/bash
```

### Frontend not starting

```bash
# Check logs
docker-compose logs frontend

# Rebuild with no cache
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### Network scanning not working

```bash
# Verify nmap is installed
docker-compose exec backend nmap --version

# Test scan
docker-compose exec backend nmap -sn 192.168.1.0/24

# Check capabilities
docker-compose exec backend capsh --print
```

### Permission errors

```bash
# Fix ownership of volumes
sudo chown -R $USER:$USER backend/data

# Or run with sudo
sudo docker-compose up -d
```

## Production Deployment

For production, modify docker-compose.yml:

1. Remove volume mounts
2. Set `DEBUG=False`
3. Use production build for frontend
4. Add reverse proxy (nginx)
5. Configure SSL/TLS
6. Set resource limits

Example production compose:

```yaml
services:
  backend:
    build: ./backend
    environment:
      - DEBUG=False
      - API_HOST=0.0.0.0
    # No volumes for production
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

## Updating

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose up -d --build

# Or force recreate
docker-compose up -d --force-recreate
```

## Backup

```bash
# Backup data volume
docker run --rm \
  -v redsec-dashboard_backend_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/data-backup.tar.gz /data

# Restore
docker run --rm \
  -v redsec-dashboard_backend_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/data-backup.tar.gz -C /
```

## Clean Up

```bash
# Stop and remove containers
docker-compose down

# Remove volumes too
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Complete cleanup
docker system prune -a --volumes
```

## Health Checks

Both services have health checks configured:

```bash
# Check health status
docker-compose ps

# Should show (healthy) for both services
```

## Environment Variables

Create `.env` file in project root:

```env
# Backend
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Database (future)
DATABASE_URL=sqlite:///./data/redsec.db

# Security
SECRET_KEY=your-secret-key-change-this

# CORS
CORS_ORIGINS=http://localhost:5173
```

## Next Steps

1. Access http://localhost:5173
2. Navigate to Network Scanner
3. Click "Start Scan"
4. View discovered devices

For more information, see [README.md](../README.md).
