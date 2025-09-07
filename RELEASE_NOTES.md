# 🎉 Benutzerverwaltung v1.0.0

Complete Flask User Management Application for Windows & macOS

## 📦 Downloads

### macOS
- **Benutzerverwaltung.dmg** - Standard version (runs in background)
- **Benutzerverwaltung-Tray.dmg** - Tray version with menu bar icon ⭐ **RECOMMENDED**

### Windows  
- Use build scripts to create .exe files (see documentation)

## ✨ Features

### Both Versions
- ✅ Complete user management (Create, Read, Update, Delete)
- ✅ SQLite database with UUID, firstname, lastname
- ✅ Web-based interface (HTML/CSS/JavaScript)
- ✅ Cross-platform data storage (~/Documents/Benutzerverwaltung/)
- ✅ Automatic browser opening
- ✅ No Python/Flask installation required

### Tray Version (Recommended) 🆕
- 📍 **Visible system tray icon** in macOS menu bar
- 🖱️ **Right-click menu** with options:
  - Open Application
  - Open Data Folder  
  - Quit Application
- 🎯 **Professional user experience** with proper app control
- 🚀 **No more hidden processes!**

## 🚀 Quick Start

### macOS Installation
1. Download **Benutzerverwaltung-Tray.dmg** (recommended)
2. Mount DMG and drag app to Applications folder
3. Double-click app → menu bar icon appears
4. Browser opens automatically at http://127.0.0.1:5000

### Windows Installation
```cmd
git clone https://github.com/ghaslbe/flask-react-windows-macos-app.git
cd flask-react-windows-macos-app
pip install -r requirements.txt
python build_windows_tray.py
```

## 🎨 Custom Icons
- 3 built-in icon styles (modern, database, gear)
- Easy custom icon integration
- See [EIGENES_ICON.md](EIGENES_ICON.md)

## 📖 Full Documentation
- [BUILD_ANLEITUNG.md](BUILD_ANLEITUNG.md) - Complete build guide
- [SCHNELLSTART.md](SCHNELLSTART.md) - Quick start
- [README.md](README.md) - Full project overview

## 🔧 Technical Details
- **Backend:** Flask + SQLite
- **Frontend:** HTML/CSS/JavaScript (embedded)
- **Build:** PyInstaller for standalone executables
- **Icons:** PIL-generated with custom designs
- **Tray:** pystray for cross-platform system tray

Perfect for small teams, personal projects, or learning Flask deployment!

## 📁 File Sizes
- **Benutzerverwaltung.dmg**: ~47.6 MB (Standard)
- **Benutzerverwaltung-Tray.dmg**: ~48.4 MB (Tray)

---
🤖 Built with Claude Code