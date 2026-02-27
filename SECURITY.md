# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

1. **Do not** open a public GitHub issue for security vulnerabilities.
2. Email the maintainers (or open a private security advisory on GitHub).
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- We will acknowledge receipt within 48 hours.
- We will provide an initial assessment within 7 days.
- We will keep you informed of progress and any planned fix.

### Scope

This project is designed for **simulation and research only**. It does not:

- Connect to live exchanges by default
- Store or transmit real API keys in any example or sample code
- Execute real trades

If you find a vulnerability that could affect users who have integrated real exchange connectors (implemented outside this repo), please report it so we can document mitigations.

### Best Practices for Users

- **Never commit** `.env` files or files containing API keys, secrets, or credentials.
- Use environment variables or a secrets manager for any sensitive configuration.
- Run the lab in isolated environments (containers, VMs) when experimenting.
- Review exchange Terms of Service and rate limits before any integration.
