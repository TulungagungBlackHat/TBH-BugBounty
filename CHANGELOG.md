# Changelog

## Unreleased

- Ecosystem standardization: SECURITY.md, CONTRIBUTING.md, requirements, CI smoke checks.

## 1.0.0 (2026-09-18)

- Initial stable single-tool release (educational, authorized-use only).

## [3.0.0] - 2026-10-10
### Added
- 6 security headers audited, technology disclosure check (X-Powered-By)
- Structured findings with severity + fix for report drafting
- Unified TBH v3 CLI: --proxy, --cookie, -H, --timeout, --json, --html, --version
- Exit codes (1 on Medium/High findings), JSON report schema
### Fixed
- Bare except blocks, utcnow deprecation, socket leak on port probe
