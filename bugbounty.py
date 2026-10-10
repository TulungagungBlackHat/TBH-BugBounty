#!/usr/bin/env python3
"""TBH-BugBounty v3 - First-pass hunter recon with report-ready output (authorized testing only)."""
import argparse, json, os, socket, ssl, sys
from datetime import datetime, timezone
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("[!] requests required: pip install requests", file=sys.stderr)
    sys.exit(2)

VERSION = "3.0"
REPO = "https://github.com/TulungagungBlackHat/TBH-BugBounty"

def banner():
    if os.environ.get("NO_COLOR"):
        return ""
    return ("\033[91m╔════════════════════════════════════╗\n"
            "║ \033[97mTBH-BugBounty v3\033[91m - Report Ready    \033[91m║\n"
            "║ \033[90mTulungagung Black Hat | uchil404 \033[91m║\n"
            "╚════════════════════════════════════╝\033[0m")

def color(code, text, enabled=True):
    return f"\033[{code}m{text}\033[0m" if enabled else text

def build_session(args):
    s = requests.Session()
    s.headers["User-Agent"] = f"TBH-BugBounty/{VERSION} (+{REPO})"
    if args.cookie:
        s.headers["Cookie"] = args.cookie
    for h in args.header or []:
        name, _, val = h.partition(":")
        if val:
            s.headers[name.strip()] = val.strip()
    if args.proxy:
        s.proxies = {"http": args.proxy, "https": args.proxy}
    return s

def recon(url, args):
    parsed = urlparse(url if "://" in url else "https://" + url)
    domain = parsed.hostname or parsed.netloc
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        return None, domain, None
    print(color("96", f"[*] Target: {domain} ({ip})", True))
    session = build_session(args)
    report = {"tool": "TBH-BugBounty", "version": VERSION, "target": domain, "ip": ip,
              "url": url, "time": str(datetime.now(timezone.utc)), "findings": []}

    try:
        r = session.get(url, timeout=args.timeout)
        important = ["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options",
                     "X-Content-Type-Options", "Referrer-Policy", "Permissions-Policy"]
        missing = [h for h in important if h not in r.headers]
        report["headers"] = {"status": r.status_code, "server": r.headers.get("Server", ""),
                             "missing": missing, "powered_by": r.headers.get("X-Powered-By", "")}
        for h in missing:
            report["findings"].append({"severity": "Low", "title": f"Missing {h}",
                                       "detail": f"HTTP {r.status_code}", "fix": f"Set {h} header"})
        print(color("96", f"[+] Headers: {r.status_code} | Missing: {', '.join(missing) or 'none'}", True))
        if r.headers.get("X-Powered-By"):
            report["findings"].append({"severity": "Info", "title": "Technology disclosed",
                                       "detail": r.headers["X-Powered-By"], "fix": "Suppress X-Powered-By"})
    except requests.RequestException as e:
        report["headers"] = {"error": str(e)}
        print(color("90", f"[-] Headers: {e}", True))

    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(args.timeout)
            s.connect((domain, 443))
            cert = s.getpeercert()
        expire = cert["notAfter"]
        days = (datetime.strptime(expire, "%b %d %H:%M:%S %Y %Z")
                .replace(tzinfo=timezone.utc) - datetime.now(timezone.utc)).days
        report["ssl"] = {"expire": expire, "days": days}
        print(color("96", f"[+] SSL: {days} days until expiry", True))
        if days < 30:
            report["findings"].append({"severity": "Medium", "title": f"SSL cert expires in {days} days",
                                       "detail": expire, "fix": "Renew certificate"})
    except Exception as e:
        report["ssl"] = {"note": f"no usable https: {e}"}

    open_ports = []
    for p in [80, 443, 8080, 8443]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(args.timeout if args.timeout <= 2 else 1.0)
        if s.connect_ex((ip, p)) == 0:
            open_ports.append(p)
            print(color("96", f"[OPEN] {p}", True))
        s.close()
    report["ports"] = open_ports

    subs = []
    for sub in ["www", "api", "admin", "test", "dev"]:
        try:
            sip = socket.gethostbyname(f"{sub}.{domain}")
            subs.append({"host": f"{sub}.{domain}", "ip": sip})
        except socket.gaierror:
            pass
    report["subdomains"] = [s["host"] for s in subs]
    return report, domain, ip

def main():
    parser = argparse.ArgumentParser(description=f"TBH-BugBounty v{VERSION}")
    parser.add_argument("-u", "--url", required=True)
    parser.add_argument("--proxy", help="e.g. http://127.0.0.1:8080")
    parser.add_argument("--cookie", help="Cookie header value")
    parser.add_argument("-H", "--header", action="append", help="extra header, repeatable")
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--json", help="save JSON")
    parser.add_argument("--html", help="save HTML report")
    parser.add_argument("--no-color", action="store_true")
    parser.add_argument("--version", action="version", version=f"TBH-BugBounty {VERSION}")
    args = parser.parse_args()
    print(banner())

    use_color = not args.no_color and not os.environ.get("NO_COLOR")
    print(color("91", "[!] Authorized targets only.", use_color))
    report, domain, ip = recon(args.url, args)
    if report is None:
        print(color("91", f"[!] cannot resolve {domain}", use_color), file=sys.stderr)
        sys.exit(2)

    print("\n--- Report suggestions ---")
    if not report["findings"]:
        print("(no automated findings - manual testing time)")
    for f in report["findings"]:
        print(f"- [{f['severity']}] {f['title']}: {f['fix']}")

    if args.json:
        try:
            with open(args.json, "w") as fh:
                json.dump(report, fh, indent=2)
            print(f"[✓] JSON: {args.json}")
        except OSError as e:
            print(color("91", f"[!] cannot write JSON: {e}", use_color), file=sys.stderr)
            sys.exit(2)
    if args.html:
        html = f"""<html><head><title>TBH-BugBounty {report['target']}</title></head>
<body style="font-family:monospace;background:#0d1117;color:#c9d1d9;padding:20px">
<h1 style="color:#ff0000">TBH-BugBounty v{VERSION} Report - {report['target']} ({report['ip']})</h1>
<p>Time: {report['time']}</p>
<h2>Findings</h2><pre>{json.dumps(report['findings'], indent=2)}</pre>
<h2>Raw</h2><pre>{json.dumps({k: report[k] for k in ('headers', 'ssl', 'ports', 'subdomains')}, indent=2)}</pre>
<p>Generated by TBH-BugBounty v{VERSION} - Tulungagung Black Hat</p></body></html>"""
        try:
            with open(args.html, "w") as fh:
                fh.write(html)
            print(f"[✓] HTML: {args.html}")
        except OSError as e:
            print(color("91", f"[!] cannot write HTML: {e}", use_color), file=sys.stderr)
            sys.exit(2)

    sys.exit(1 if any(f["severity"] in ("High", "Medium") for f in report["findings"]) else 0)

if __name__ == "__main__":
    main()
