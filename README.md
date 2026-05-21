# website_easy
Website made for testing cybersecurity. (easy mode)

This repo intentionally contains obvious vulnerabilities for SAST testing with
Semgrep. Do not deploy it to the internet.

Useful scan command:

```bash
semgrep scan --config p/secrets --config p/python --json .
```
