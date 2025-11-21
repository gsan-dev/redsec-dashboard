# Quick Start Guide - RedSec Dashboard

## Running the Application

### Backend

```bash
cd backend

# Activate virtual environment
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Run the server
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend

# Run development server
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## Testing the Scanner

1. Open your browser to `http://localhost:5173`
2. Click the "Start Scan" button
3. Wait for the network scan to complete
4. View discovered devices in the grid

## Notes

- The scanner requires network privileges to work correctly
- On Windows, you may need to run as Administrator
- The scanner works by pinging IPs in your local network range (x.x.x.1-254)
- MAC addresses are retrieved via ARP

## Troubleshooting

**Backend won't start:**
- Check if port 8000 is available
- Verify Python dependencies are installed: `pip list`

**Scanner not finding devices:**
- Run as administrator (Windows) or with sudo (Linux)
- Check your network interface is accessible
- Verify ping is working: `ping 192.168.1.1`

**Frontend connection error:**
- Make sure backend is running on port 8000
- Check browser console for CORS errors
- Verify API_URL in frontend matches backend address
