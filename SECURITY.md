# Security Policy

## Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of RedSec Dashboard seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do Not Open a Public Issue

Please **do not** create a public GitHub issue for security vulnerabilities.

### 2. Report Privately

Send an email to: **security@redsec-dashboard.example.com** (replace with your actual security contact)

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Response Timeline

- **24 hours:** Initial response acknowledging receipt
- **7 days:** Assessment and triage of the vulnerability
- **30 days:** Fix developed and tested
- **Release:** Security patch released

### 4. Coordinated Disclosure

We follow responsible disclosure practices:
- We'll work with you to understand and fix the issue
- We'll credit you in the security advisory (unless you prefer to remain anonymous)
- We'll coordinate the public disclosure timeline

## Security Best Practices

### For Users

1. **Keep Updated:** Always use the latest version
2. **Strong Credentials:** Use strong passwords and API keys
3. **Limit Access:** Run with least privileges when possible
4. **HTTPS:** Use SSL/TLS in production
5. **Firewall:** Restrict network access appropriately
6. **Review Logs:** Monitor for suspicious activity

### For Developers

1. **Input Validation:** Always validate and sanitize inputs
2. **Dependencies:** Keep dependencies updated
3. **Secrets:** Never commit secrets or credentials
4. **Code Review:** Review security-critical code carefully
5. **Testing:** Include security tests in CI/CD

## Known Security Considerations

### Network Scanning

- Nmap requires elevated privileges for OS detection
- Only run on networks you own or have permission to scan
- Be aware of local laws regarding network scanning

### API Security

- Change default SECRET_KEY in production
- Configure CORS appropriately
- Use authentication in production environments

### Docker Security

- Don't expose ports publicly without proper security
- Review Docker configuration for production
- Use non-root users when possible

## Security Features

- **Plugin Isolation:** Plugins run in isolated environments
- **Input Validation:** All API inputs are validated
- **CORS Protection:** Configurable CORS policies
- **SQL Injection Protection:** Using SQLAlchemy ORM

## Acknowledgments

We thank the security researchers who responsibly disclose vulnerabilities to us.

Hall of Fame:
- (Your name could be here!)

## Contact

For non-security issues, use GitHub Issues.
For security concerns, email: security@redsec-dashboard.example.com
