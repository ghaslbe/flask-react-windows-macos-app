# flask-react-windows-macos-app

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

### Windows
1. `Benutzerverwaltung.exe` herunterladen
2. Doppelklick → fertig!

### macOS  
1. `Benutzerverwaltung.dmg` herunterladen
2. DMG mounten → App zu Applications ziehen
3. Doppelklick → fertig!

**Daten werden gespeichert in:**
- Windows: `%USERPROFILE%\Documents\Benutzerverwaltung\`
- macOS: `~/Documents/Benutzerverwaltung/`

## 🛠️ Für Entwickler

### Schnellstart

**Windows:**
```cmd
build_all.bat
```

**macOS:**
```bash
python build_macos.py
python create_dmg.py
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
python app_exe.py
```
→ Browser öffnet sich auf http://127.0.0.1:5000

### Build-Prozess
Siehe detaillierte Anleitung in:
- [`BUILD_ANLEITUNG.md`](BUILD_ANLEITUNG.md) - Vollständige Anleitung
- [`SCHNELLSTART.md`](SCHNELLSTART.md) - Kurze Version

## 📁 Projektstruktur

```
├── app_exe.py              # Hauptanwendung
├── requirements.txt        # Python Dependencies  
├── build_exe.py           # Windows Build
├── build_macos.py         # macOS Build
├── create_dmg.py          # DMG Erstellung
├── build_all.bat          # Windows Auto-Build
├── test_app.py            # Tests
└── dist/                  # Build-Ergebnisse
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