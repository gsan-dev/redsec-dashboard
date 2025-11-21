# Contributing to RedSec Dashboard

First off, thank you for considering contributing to RedSec Dashboard! It's people like you that make RedSec Dashboard such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples**
* **Describe the behavior you observed and what you expected**
* **Include screenshots if possible**
* **Include your environment details** (OS, Python version, Node version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the suggested enhancement**
* **Explain why this enhancement would be useful**
* **List any alternative solutions you've considered**

### Pull Requests

* Fill in the required template
* Follow the Python and TypeScript style guides
* Include tests when adding new features
* Update documentation as needed
* End all files with a newline

## Development Process

### Setting Up Your Development Environment

1. Fork the repo
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/redsec-dashboard.git
   cd redsec-dashboard
   ```

3. Create a branch:
   ```bash
   git checkout -b feature/my-new-feature
   ```

4. Make your changes and commit:
   ```bash
   git add .
   git commit -m "Add some feature"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/my-new-feature
   ```

6. Create a Pull Request

### Coding Standards

#### Python (Backend)

* Follow PEP 8
* Use type hints
* Write docstrings for all public methods
* Keep functions focused and small
* Use meaningful variable names

Example:
```python
async def scan_network(self, network_range: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Scan the network for active devices.
    
    Args:
        network_range: Optional CIDR notation network range
        
    Returns:
        List of discovered devices with their information
    """
    pass
```

#### TypeScript (Frontend)

* Use TypeScript strict mode
* Follow React best practices
* Use functional components with hooks
* Keep components small and focused
* Use meaningful component and prop names

Example:
```typescript
interface ScannerProps {
  onScanComplete?: (devices: Device[]) => void;
}

export const Scanner: React.FC<ScannerProps> = ({ onScanComplete }) => {
  // Component logic
};
```

### Testing

* Write tests for new features
* Ensure all tests pass before submitting PR
* Maintain or improve code coverage

**Testing Backend:**
```bash
cd backend
pytest
```

**Testing Frontend:**
```bash
cd frontend
npm test
```

### Plugin Development

If you're developing a new plugin:

1. Follow the plugin template structure
2. Include `plugin.json` with complete metadata
3. Implement all required BasePlugin methods
4. Add tests for your plugin
5. Update plugin documentation

See [Plugin Development Guide](docs/PLUGIN_DEVELOPMENT.md) for details.

### Documentation

* Update README.md if needed
* Add docstrings/comments for complex logic
* Update API documentation
* Create/update relevant guides in `docs/`

### Commit Messages

* Use clear and meaningful commit messages
* Start with a verb in present tense (Add, Fix, Update, Remove)
* Reference issues when applicable

Good examples:
```
Add bandwidth monitoring plugin
Fix scanner crash on empty network range
Update installation docs for Ubuntu 24.04
Remove deprecated API endpoint
```

## Project Structure

```
redsec-dashboard/
├── backend/           # Python/FastAPI backend
├── frontend/          # React/TypeScript frontend
├── docs/             # Documentation
├── tests/            # Test files
└── README.md         # Main documentation
```

## Getting Help

* Check the [documentation](docs/)
* Search existing [issues](https://github.com/yourusername/redsec-dashboard/issues)
* Ask in [discussions](https://github.com/yourusername/redsec-dashboard/discussions)

## Recognition

Contributors will be recognized in:
* README.md contributors section
* Release notes
* Project documentation

Thank you for contributing to RedSec Dashboard! 🎉
