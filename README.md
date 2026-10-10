# TBH-BugBounty

<p align="center">
  <a href="https://github.com/TulungagungBlackHat/TBH-BugBounty/actions/workflows/ci.yml"><img src="https://github.com/TulungagungBlackHat/TBH-BugBounty/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-red.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/output-JSON%20%7C%20HTML-orange.svg" alt="JSON HTML">
</p>

Bug bounty hunter's first-pass toolkit: security headers, SSL expiry, open ports, and report-ready output — structured for HackerOne/Bugcrowd submissions.

Part of the [Tulungagung Black Hat](https://github.com/TulungagungBlackHat) toolset.

## What It Collects

- **Security headers** — missing HSTS, CSP, X-Frame-Options, etc. with severity hints
- **SSL certificate** — days until expiry (expiring cert = Medium finding)
- **Open ports** — common service ports with status
- **Report suggestions** — auto-drafted findings list with severities, ready to paste into your report template

Output as JSON (for tooling) or HTML (for sharing).

## Install

```bash
git clone https://github.com/TulungagungBlackHat/TBH-BugBounty
cd TBH-BugBounty
pip install -r requirements.txt
```

## Usage

```
usage: bugbounty.py [-h] -u URL [--json JSON] [--html HTML]

options:
  -u, --url URL     Target URL
  --json JSON       Save JSON report
  --html HTML       Save HTML report
```

```bash
python3 bugbounty.py -u https://example.com --json report.json --html report.html
```

## Sample Output

```
[*] Target: example.com (93.184.216.34)
[+] Headers: 200 | Missing: strict-transport-security, content-security-policy
[+] SSL: 42 days
[OPEN] 80
[OPEN] 443

--- Saran Laporan ---
- Missing strict-transport-security, content-security-policy (Low)
- SSL 42 days (Medium)
```

Treat the suggestions as a starting checklist — verify each one, add reproduction steps, and write the report in the program's format.

## Authorized Use Only

Only against scopes you own or are authorized to test. See [SECURITY.md](SECURITY.md).

## Related Tools

- [TBH-Recon](https://github.com/TulungagungBlackHat/TBH-Recon) — deeper recon with subdomains
- [TBH-AllScan](https://github.com/TulungagungBlackHat/TBH-AllScan) — 10 active modules plus risk score

## License

[MIT](LICENSE) — Tulungagung Black Hat, East Java, Indonesia. Always Smile :)
