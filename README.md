# TBH-BugBounty - Hunter Toolkit

<p align="center">
  <img src="https://img.shields.io/badge/Bug%20Bounty-Hunter-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Scope-Only%20Authorized-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/TBH-Tulungagung%20Black%20Hat-black?style=for-the-badge">
</p>

> **Hanya untuk scope yang diizinkan** di HackerOne/Bugcrowd. Jangan scan target tanpa izin.

## ✨ Features
- 🔍 **Header Misconfig** → auto saran laporan Low
- 🔐 **SSL Expire Check** → saran Medium jika <30 hari
- 🚪 **Port Quick** 80,443,8080,8443
- 🌐 **Subdomain** www,api,admin,test
- 📄 **JSON Export** siap lampiran HackerOne

## 🚀 Usage
```bash
git clone https://github.com/TulungagungBlackHat/TBH-BugBounty
cd TBH-BugBounty
python3 bugbounty.py -u https://example.com --json report.json
cat report.json
```

## 📝 Cara Lapor
1. Pillih missing header → buat title `Missing CSP`
2. Sertakan PoC dari `report.json`
3. Jelaskan dampak & fix

## 👥 TBH
uchil404 - Tulungagung Black Hat - Always Smile :)

## 📄 License
MIT - Edukasi
