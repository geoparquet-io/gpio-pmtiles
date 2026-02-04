# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take the security of gpio-pmtiles seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please do NOT:

- Open a public GitHub issue for security vulnerabilities
- Disclose the vulnerability publicly before it has been addressed

### Please DO:

1. **Report via GitHub Security Advisories** (preferred):
   - Go to the [Security tab](https://github.com/geoparquet/gpio-pmtiles/security/advisories)
   - Click "Report a vulnerability"
   - Fill in the details

2. **Email**: If you prefer, you can email the maintainers at:
   - cholmes@9eo.org
   - Use subject line: "SECURITY: gpio-pmtiles - [brief description]"

### What to include:

- Type of vulnerability (e.g., path traversal, command injection, etc.)
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### What to expect:

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days with our evaluation
- **Fix Timeline**: Critical issues within 30 days, others within 90 days
- **Credit**: We will acknowledge your contribution in the release notes (unless you prefer to remain anonymous)

## Security Best Practices for Users

When using gpio-pmtiles:

1. **Keep Dependencies Updated**
   - Regularly update to the latest version
   - Run `uv sync` or `pip install --upgrade gpio-pmtiles`
   - Monitor security advisories

2. **Input Validation**
   - Validate file paths before processing
   - Be cautious when processing files from untrusted sources
   - Verify output paths to prevent overwrites

3. **File Permissions**
   - Ensure proper file permissions on output directories
   - Don't run with elevated privileges unless necessary
   - Be aware of symlink attacks when processing files

4. **Tippecanoe Dependency**
   - This plugin shells out to the `tippecanoe` command
   - Ensure tippecanoe is from a trusted source
   - Keep tippecanoe updated

## Known Security Considerations

### File Processing
- This plugin reads GeoParquet files and writes PMTiles files
- Users should validate file paths and permissions
- Processing untrusted files may expose system vulnerabilities

### External Command Execution
- The plugin executes the `tippecanoe` command via subprocess
- File paths are passed to tippecanoe
- Command injection risks are mitigated but users should validate inputs

### Dependency Chain
- Inherits security properties of geoparquet-io
- Depends on PyArrow for Parquet processing
- Uses system tippecanoe binary

## Disclosure Policy

- Security vulnerabilities will be disclosed after a fix is available
- We will publish a security advisory on GitHub
- Critical vulnerabilities will be highlighted in release notes
- CVE IDs will be requested for significant vulnerabilities

## Security Updates

Security updates are delivered through:
- GitHub Security Advisories
- Release notes in CHANGELOG.md
- PyPI package updates
- GitHub Releases

## Questions?

If you have questions about security that are not vulnerabilities, please:
- Open a regular GitHub issue
- Contact maintainers via email

Thank you for helping keep gpio-pmtiles and its users safe!
