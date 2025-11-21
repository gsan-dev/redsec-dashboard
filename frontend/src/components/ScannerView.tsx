import { useState } from 'react';
import './ScannerView.css';

interface Device {
    ip: string;
    mac: string;
    hostname: string;
    vendor: string;
    status: string;
    first_seen: string;
    last_seen: string;
    ports: number[];
}

interface ScanResponse {
    status: string;
    action: string;
    devices: Device[];
    total: number;
}

function ScannerView() {
    const [devices, setDevices] = useState<Device[]>([]);
    const [isScanning, setIsScanning] = useState(false);
    const [scanProgress, setScanProgress] = useState(0);
    const [error, setError] = useState<string | null>(null);

    const startScan = async () => {
        setIsScanning(true);
        setError(null);
        setScanProgress(0);

        // Simulate progress (since the backend scan is async)
        const progressInterval = setInterval(() => {
            setScanProgress(prev => {
                if (prev >= 90) {
                    clearInterval(progressInterval);
                    return prev;
                }
                return prev + 10;
            });
        }, 500);

        try {
            const response = await fetch('/api/scan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ network: null }),
            });

            if (!response.ok) {
                throw new Error('Scan failed');
            }

            const data: ScanResponse = await response.json();
            setDevices(data.devices || []);
            setScanProgress(100);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred during scanning');
        } finally {
            clearInterval(progressInterval);
            setTimeout(() => {
                setIsScanning(false);
                setScanProgress(0);
            }, 500);
        }
    };

    const getStatusColor = (status: string) => {
        return status === 'active' ? 'var(--accent-success)' : 'var(--accent-danger)';
    };

    return (
        <div className="scanner-view">
            <div className="scanner-header">
                <div>
                    <h2 className="mb-0">Network Scanner</h2>
                    <p className="text-muted" style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
                        Discover and monitor devices on your network
                    </p>
                </div>
                <button
                    className="btn btn-primary"
                    onClick={startScan}
                    disabled={isScanning}
                >
                    {isScanning ? (
                        <>
                            <div className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }}></div>
                            Scanning...
                        </>
                    ) : (
                        <>
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                <path d="M8 2V8L12 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                                <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="2" fill="none" />
                            </svg>
                            Start Scan
                        </>
                    )}
                </button>
            </div>

            {isScanning && (
                <div className="scan-progress fade-in">
                    <div className="progress-bar">
                        <div
                            className="progress-fill"
                            style={{ width: `${scanProgress}%` }}
                        ></div>
                    </div>
                    <p className="text-muted" style={{ textAlign: 'center', fontSize: '0.875rem', marginTop: '0.5rem' }}>
                        Scanning network... {scanProgress}%
                    </p>
                </div>
            )}

            {error && (
                <div className="card fade-in" style={{ borderColor: 'var(--accent-danger)', background: 'rgba(239, 68, 68, 0.05)' }}>
                    <p style={{ color: 'var(--accent-danger)', margin: 0 }}>❌ {error}</p>
                </div>
            )}

            {devices.length > 0 && (
                <div className="devices-section fade-in">
                    <div className="devices-stats">
                        <div className="stat-card">
                            <div className="stat-value">{devices.length}</div>
                            <div className="stat-label">Total Devices</div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-value">{devices.filter(d => d.status === 'active').length}</div>
                            <div className="stat-label">Active</div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-value">{devices.filter(d => d.hostname).length}</div>
                            <div className="stat-label">Identified</div>
                        </div>
                    </div>

                    <div className="devices-grid">
                        {devices.map((device, index) => (
                            <div key={device.ip} className="device-card card" style={{ animationDelay: `${index * 50}ms` }}>
                                <div className="device-header">
                                    <div className="flex items-center gap-sm">
                                        <div
                                            className="status-indicator pulse"
                                            style={{ backgroundColor: getStatusColor(device.status) }}
                                        ></div>
                                        <h3 className="mb-0" style={{ fontSize: '1rem' }}>
                                            {device.hostname || device.ip}
                                        </h3>
                                    </div>
                                    <span className="badge badge-success">{device.status}</span>
                                </div>

                                <div className="device-info">
                                    <div className="info-row">
                                        <span className="info-label">IP Address:</span>
                                        <span className="info-value">{device.ip}</span>
                                    </div>
                                    {device.mac && (
                                        <div className="info-row">
                                            <span className="info-label">MAC Address:</span>
                                            <span className="info-value">{device.mac}</span>
                                        </div>
                                    )}
                                    {device.vendor && (
                                        <div className="info-row">
                                            <span className="info-label">Vendor:</span>
                                            <span className="info-value">{device.vendor}</span>
                                        </div>
                                    )}
                                    {device.hostname && device.hostname !== device.ip && (
                                        <div className="info-row">
                                            <span className="info-label">Hostname:</span>
                                            <span className="info-value">{device.hostname}</span>
                                        </div>
                                    )}
                                </div>

                                <div className="device-footer">
                                    <span className="text-muted" style={{ fontSize: '0.75rem' }}>
                                        Last seen: {new Date(device.last_seen).toLocaleTimeString()}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {!isScanning && devices.length === 0 && !error && (
                <div className="empty-state card">
                    <svg width="64" height="64" viewBox="0 0 64 64" fill="none" style={{ margin: '0 auto' }}>
                        <circle cx="32" cy="32" r="30" stroke="var(--accent-primary)" strokeWidth="2" strokeDasharray="4 4" opacity="0.3" />
                        <path d="M32 20L24 26V38L32 44L40 38V26L32 20Z" stroke="var(--accent-primary)" strokeWidth="2" fill="none" />
                        <circle cx="32" cy="32" r="4" fill="var(--accent-primary)" />
                    </svg>
                    <h3 style={{ textAlign: 'center', marginTop: '1.5rem' }}>No Devices Found</h3>
                    <p className="text-muted" style={{ textAlign: 'center' }}>
                        Click "Start Scan" to discover devices on your network
                    </p>
                </div>
            )}
        </div>
    );
}

export default ScannerView;
