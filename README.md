# flask-react-windows-macos-app

[![GitHub release](https://img.shields.io/github/v/release/ghaslbe/flask-react-windows-macos-app)](https://github.com/ghaslbe/flask-react-windows-macos-app/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/ghaslbe/flask-react-windows-macos-app/total)](https://github.com/ghaslbe/flask-react-windows-macos-app/releases)

🚀 **Benutzerverwaltung als Standalone-App für Windows & macOS**

Eine einfache Benutzerverwaltung mit Flask Backend und Web-Frontend, verpackt als eigenständige Anwendung für Windows (.exe) und macOS (.dmg).

## ✨ Features

- 📝 **CRUD Operations**: Benutzer erstellen, bearbeiten, löschen
- 🆔 **UUID**: Eindeutige Benutzer-IDs
- 💾 **SQLite**: Lokale Datenspeicherung
- 🌐 **Web Interface**: HTML/CSS/JavaScript Frontend
- 📦 **Standalone**: Keine Installation von Python/Flask erforderlich
- 🖥️ **Cross-Platform**: Windows EXE & macOS DMG
- 🔄 **Auto-Start**: Browser öffnet automatisch

## 🎯 Für Endnutzer

### 📦 Fertige Downloads (v1.0.0)

**macOS (sofort einsatzbereit):**
- 🔗 [**Benutzerverwaltung-Tray.dmg**](https://github.com/ghaslbe/flask-react-windows-macos-app/releases/latest/download/Benutzerverwaltung-Tray.dmg) ⭐ **EMPFOHLEN** (Tray-Version)
- 🔗 [Benutzerverwaltung.dmg](https://github.com/ghaslbe/flask-react-windows-macos-app/releases/latest/download/Benutzerverwaltung.dmg) (Standard-Version)

**Windows:**
- 📁 Repository clonen und mit Build-Scripts erstellen (siehe unten)

## 🎯 Installation

### Standard Version (unsichtbar im Hintergrund)
**Windows:**
1. `Benutzerverwaltung.exe` herunterladen
2. Doppelklick → fertig!

**macOS:**
1. `Benutzerverwaltung.dmg` herunterladen  
2. DMG mounten → App zu Applications ziehen
3. Doppelklick → fertig!

### Tray Version (mit Taskleisten-Icon) 🆕
**Windows:**
1. `Benutzerverwaltung-Tray.exe` herunterladen
2. Doppelklick → Icon erscheint in der Taskleiste

**macOS:**
1. `Benutzerverwaltung-Tray.dmg` herunterladen
2. App installieren → Icon erscheint in der Menüleiste

### 🤔 Warum läuft die App "unsichtbar"?

**Bei der Standard-Version:**
- ✅ App läuft als **Background-Prozess**
- ❌ **Kein Fenster** oder Dock-Icon sichtbar
- 🌐 **Browser öffnet automatisch** für die Bedienung
- 🔍 **Sichtbar in:** Aktivitätsanzeige (macOS) / Task-Manager (Windows)

**Bei der Tray-Version:**
- ✅ **System Tray Icon** (Windows Taskleiste / macOS Menüleiste)
- 🖱️ **Rechtsklick** für Optionen-Menü
- 🚀 **App öffnen**, **Datenordner** anzeigen, **Beenden**

**Daten werden gespeichert in:**
- Windows: `%USERPROFILE%\Documents\Benutzerverwaltung\`
- macOS: `~/Documents/Benutzerverwaltung/`

## 🛠️ Für Entwickler

### Schnellstart

**Build für macOS:**
```bash
# Standard Version
pyinstaller Benutzerverwaltung.spec

# Tray Version
pyinstaller Benutzerverwaltung-Tray.spec

# DMG erstellen (optional)
python build_macos.py
```

**Build für Windows:**
- Mit entsprechender .spec Datei und PyInstaller

### Installer-Pakete erstellen

**macOS (.pkg erstellen):**
```bash
# Nach PyInstaller Build
pkgbuild --root dist/Benutzerverwaltung-Tray.app \
         --identifier com.example.benutzerverwaltung-tray \
         --version 1.0 \
         --install-location /Applications \
         Benutzerverwaltung-Tray.pkg
```

**Windows (.msi erstellen):**
```bash
# WiX Toolset erforderlich
candle installer.wxs
light -ext WixUIExtension installer.wixobj -out Benutzerverwaltung.msi
```

### Voraussetzungen
- Python 3.8+
- pip

### Installation
```bash
git clone https://github.com/ghaslbe/flask-react-windows-macos-app.git
cd flask-react-windows-macos-app
pip install -r requirements.txt
```

### Entwicklung
```bash
python app.py
```
→ Browser öffnet sich auf http://127.0.0.1:5000

### Build-Prozess
Siehe detaillierte Anleitung in:
- [`BUILD_ANLEITUNG.md`](BUILD_ANLEITUNG.md) - Vollständige Anleitung
- [`SCHNELLSTART.md`](SCHNELLSTART.md) - Kurze Version

## 📁 Projektstruktur

```
├── app.py                   # Hauptanwendung (Standard & Tray Support)
├── requirements.txt         # Python Dependencies  
├── Benutzerverwaltung.spec  # PyInstaller Konfiguration (Standard)
├── Benutzerverwaltung-Tray.spec # PyInstaller Konfiguration (Tray)
├── build_macos.py          # macOS Build Script
├── create_icons.py         # Icon-Generator
├── test_app.py             # Tests
├── icons/                  # App-Icons (verschiedene Formate)
└── dist/                   # Build-Ergebnisse
```

## 🔧 Technische Details

- **Backend**: Flask + SQLite
- **Frontend**: HTML/CSS/JavaScript (eingebettet)
- **Packaging**: PyInstaller
- **Datenbank**: SQLite (automatische Erstellung)
- **Cross-Platform**: Windows, macOS, Linux

## 🎨 Screenshots

Die App öffnet automatisch im Browser mit einem benutzerfreundlichen Interface für:
- Benutzer hinzufügen (Vorname + Nachname)
- Benutzer-Tabelle mit Bearbeiten/Löschen
- Responsive Design

## 🤝 Beitragen

1. Fork das Repository
2. Feature Branch erstellen (`git checkout -b feature/neue-funktion`)
3. Änderungen committen (`git commit -m 'Neue Funktion hinzugefügt'`)
4. Branch pushen (`git push origin feature/neue-funktion`)
5. Pull Request erstellen

## 📜 Lizenz

Dieses Projekt steht unter der MIT Lizenz - siehe [LICENSE](LICENSE) für Details.

## 🐛 Probleme melden

Bei Problemen bitte ein [Issue](https://github.com/ghaslbe/flask-react-windows-macos-app/issues) erstellen.

---

**Erstellt mit ❤️ für einfache Cross-Platform Distribution von Flask-Apps**