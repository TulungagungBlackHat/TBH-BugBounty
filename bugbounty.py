#!/usr/bin/env python3
# TBH-BugBounty - Bug Bounty Recon Toolkit (Educational)
# Tulungagung Black Hat - uchil404 | Only for Authorized Scope
import socket, requests, argparse, json, ssl
from datetime import datetime
from urllib.parse import urlparse

BANNER = """\033[91m╔════════════════════════════════════╗
\033[91m║ \033[97mTBH-BugBounty \033[91m- Hunter Toolkit     \033[91m║
\033[91m║ \033[90mTulungagung Black Hat | uchil404 \033[91m║
\033[91m╚════════════════════════════════════╝\033[0m"""

def recon(url):
    domain=urlparse(url if url.startswith("http") else "https://"+url).netloc
    ip=socket.gethostbyname(domain)
    print(f"[*] Target: {domain} ({ip})")
    report={"target":domain,"ip":ip,"url":url,"time":str(datetime.now())}
    # Headers
    try:
        r=requests.get(url,timeout=5,headers={'User-Agent':'TBH-BugBounty/1.0'})
        missing=[h for h in ['Content-Security-Policy','Strict-Transport-Security','X-Frame-Options'] if h not in r.headers]
        report["headers"]={"status":r.status_code,"server":r.headers.get('Server','Unknown'),"missing":missing}
        print(f"[+] Headers: {r.status_code} | Missing: {missing or 'none'}")
        if missing:
            print(f"  -> Potensi Low: Missing {missing} -> laporkan sebagai Security Misconfiguration")
    except Exception as e: report["headers"]={"error":str(e)}
    # SSL
    try:
        ctx=ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(),server_hostname=domain) as s:
            s.settimeout(3); s.connect((domain,443)); cert=s.getpeercert()
            expire=cert.get('notAfter'); days=(datetime.strptime(expire,"%b %d %H:%M:%S %Y %Z")-datetime.utcnow()).days
            report["ssl"]={"expire":expire,"days":days}
            print(f"[+] SSL: {days} days left")
            if days<30: print("  -> Potensi Medium: SSL expire soon")
    except: report["ssl"]={"note":"no https or fail"}
    # Ports quick
    common=[80,443,8080,8443]
    open_ports=[]
    for p in common:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.settimeout(1)
        if s.connect_ex((ip,p))==0: open_ports.append(p); print(f"[OPEN] {p}")
        s.close()
    report["ports"]=open_ports
    # Subdomains
    found=[]
    for sub in ['www','api','admin','test']:
        try: socket.gethostbyname(f"{sub}.{domain}"); found.append(f"{sub}.{domain}"); print(f"[FOUND] {sub}.{domain}")
        except: pass
    report["subdomains"]=found
    return report

def main():
    print(BANNER)
    print("\033[91m[!] Hanya untuk scope bug bounty yang diizinkan!\033[0m\n")
    parser=argparse.ArgumentParser(description="TBH-BugBounty - Hunter Toolkit")
    parser.add_argument("-u","--url",required=True,help="Target URL dalam scope")
    parser.add_argument("--json",help="Save JSON report untuk HackerOne")
    args=parser.parse_args()
    report=recon(args.url)
    print("\n--- Saran Laporan Bug Bounty ---")
    if report["headers"].get("missing"): print(f"- Buat laporan: Missing Security Headers {report['headers']['missing']} (Low)")
    if "ssl" in report and isinstance(report["ssl"],dict) and report["ssl"].get("days",999)<30: print(f"- Laporan: SSL Expire Soon {report['ssl']['days']} days (Medium)")
    if report["ports"]: print(f"- Info: Open ports {report['ports']} - cek satu per satu")
    print("- Selalu sertakan PoC + dampak + fix di laporan")
    if args.json:
        open(args.json,'w').write(json.dumps(report,indent=2))
        print(f"\n[✓] JSON saved: {args.json} - siap upload ke HackerOne/Bugcrowd (sebagai lampiran)")

if __name__=="__main__": main()
