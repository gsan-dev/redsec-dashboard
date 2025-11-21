import { useState, useEffect } from 'react';
import ScannerView from './components/ScannerView';
import './App.css';

interface Plugin {
  name: string;
  metadata: {
    name: string;
    version: string;
    description: string;
    enabled: boolean;
  };
}

function App() {
  const [plugins, setPlugins] = useState<Plugin[]>([]);
  const [loading, setLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState<'checking' | 'connected' | 'error'>('checking');
  const [activeView, setActiveView] = useState<'dashboard' | 'scanner' | 'plugins'>('dashboard');

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const response = await fetch('/api/health');
      if (response.ok) {
        setApiStatus('connected');
        await loadPlugins();
      } else {
        setApiStatus('error');
      }
    } catch (error) {
      console.error('API health check failed:', error);
      setApiStatus('error');
    } finally {
      setLoading(false);
    }
  };

  const loadPlugins = async () => {
    try {
      const response = await fetch('/api/plugins');
      const data = await response.json();
      setPlugins(data.plugins || []);
    } catch (error) {
      console.error('Failed to load plugins:', error);
    }
  };

  const RedSecLogo = () => (
    <div className="redsec-logo">
      <div className="logo-icon">
        <div className="shield-outline">
          <div className="shield-inner"></div>
          <div className="scan-line"></div>
        </div>
      </div>
      <div className="logo-text">
        <span className="brand-red">Red</span>
        <span className="brand-sec">Sec</span>
      </div>
    </div>
  );

  return (
    <div className="app">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <RedSecLogo />
          <div className="version-badge">v1.0.0</div>
        </div>

        <nav className="sidebar-nav">
          <button
            className={`nav-item ${activeView === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveView('dashboard')}
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <rect x="2" y="2" width="7" height="7" rx="1" stroke="currentColor" strokeWidth="2" />
              <rect x="11" y="2" width="7" height="7" rx="1" stroke="currentColor" strokeWidth="2" />
              <rect x="2" y="11" width="7" height="7" rx="1" stroke="currentColor" strokeWidth="2" />
              <rect x="11" y="11" width="7" height="7" rx="1" stroke="currentColor" strokeWidth="2" />
            </svg>
            Dashboard
          </button>

          <button
            className={`nav-item ${activeView === 'scanner' ? 'active' : ''}`}
            onClick={() => setActiveView('scanner')}
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="7" stroke="currentColor" strokeWidth="2" />
              <path d="M10 3v4M10 13v4M3 10h4M13 10h4" stroke="currentColor" strokeWidth="2" />
            </svg>
            Network Scanner
          </button>

          <button
            className={`nav-item ${activeView === 'plugins' ? 'active' : ''}`}
            onClick={() => setActiveView('plugins')}
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <rect x="3" y="3" width="6" height="6" rx="1" stroke="currentColor" strokeWidth="2" />
              <rect x="11" y="3" width="6" height="6" rx="1" stroke="currentColor" strokeWidth="2" />
              <rect x="3" y="11" width="6" height="6" rx="1" stroke="currentColor" strokeWidth="2" />
              <path d="M14 14l3 3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
            Plugins
          </button>
        </nav>

        <div className="sidebar-footer">
          <div className="api-status">
            {apiStatus === 'connected' && (
              <div className="status-indicator online">
                <div className="status-left">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.5" />
                    <path d="M8 4v4l2 2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                  </svg>
                  <span>Backend API</span>
                </div>
                <div className="status-right">
                  <span className="pulse-dot"></span>
                  <span className="status-text">Online</span>
                </div>
              </div>
            )}
            {apiStatus === 'error' && (
              <div className="status-indicator offline">
                <div className="status-left">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.5" />
                    <path d="M5.5 5.5l5 5M10.5 5.5l-5 5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                  </svg>
                  <span>Backend API</span>
                </div>
                <div className="status-right">
                  <span className="pulse-dot"></span>
                  <span className="status-text">Offline</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        <div className="content-header">
          <div>
            <h1 className="page-title">
              {activeView === 'dashboard' && 'Dashboard'}
              {activeView === 'scanner' && 'Network Scanner'}
              {activeView === 'plugins' && 'Plugin Manager'}
            </h1>
            <p className="page-subtitle">
              {activeView === 'dashboard' && 'Overview of your network security'}
              {activeView === 'scanner' && 'Discover and monitor devices on your network'}
              {activeView === 'plugins' && 'Manage installed plugins and extensions'}
            </p>
          </div>
        </div>

        <div className="content-body">
          {loading ? (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Initializing RedSec Dashboard...</p>
            </div>
          ) : apiStatus === 'error' ? (
            <div className="error-state card">
              <div className="error-icon">⚠️</div>
              <h2>Backend Connection Error</h2>
              <p className="text-secondary">
                Cannot connect to the backend API. Please make sure the backend is running.
              </p>
              <div className="command-display">
                <code>cd backend && python -m uvicorn src.main:app --reload</code>
              </div>
              <button className="btn btn-primary" onClick={checkApiHealth}>
                Retry Connection
              </button>
            </div>
          ) : (
            <>
              {activeView === 'dashboard' && (
                <div className="dashboard-view fade-in">
                  <div className="stats-grid">
                    <div className="stat-card">
                      <div className="stat-icon">🔌</div>
                      <div className="stat-info">
                        <div className="stat-value">{plugins.length}</div>
                        <div className="stat-label">Active Plugins</div>
                      </div>
                    </div>
                    <div className="stat-card">
                      <div className="stat-icon">📡</div>
                      <div className="stat-info">
                        <div className="stat-value">Ready</div>
                        <div className="stat-label">Scanner Status</div>
                      </div>
                    </div>
                    <div className="stat-card">
                      <div className="stat-icon">🛡️</div>
                      <div className="stat-info">
                        <div className="stat-value">Secure</div>
                        <div className="stat-label">Network Status</div>
                      </div>
                    </div>
                  </div>

                  <div className="plugins-overview">
                    <h3>Installed Plugins</h3>
                    <div className="plugin-list">
                      {plugins.map((plugin) => (
                        <div key={plugin.name} className="plugin-item card">
                          <div className="plugin-header">
                            <h4>{plugin.metadata.name}</h4>
                            <span className="badge badge-success">Active</span>
                          </div>
                          <p className="text-secondary">{plugin.metadata.description}</p>
                          <div className="plugin-footer">
                            <span className="text-muted">v{plugin.metadata.version}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {activeView === 'scanner' && <ScannerView />}

              {activeView === 'plugins' && (
                <div className="plugins-view fade-in">
                  <div className="plugins-header">
                    <p className="text-secondary">
                      Manage and configure your installed plugins
                    </p>
                  </div>
                  <div className="plugin-grid">
                    {plugins.map((plugin) => (
                      <div key={plugin.name} className="plugin-card card">
                        <div className="plugin-icon">🔌</div>
                        <h3>{plugin.metadata.name}</h3>
                        <p className="text-secondary">{plugin.metadata.description}</p>
                        <div className="plugin-meta">
                          <span className="badge badge-success">v{plugin.metadata.version}</span>
                          <span className="badge badge-success">Enabled</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
