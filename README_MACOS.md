# Benutzerverwaltung - macOS DMG

Eine einfache Benutzerverwaltung als macOS Application Bundle, verpackt als DMG für einfache Distribution.

## 🎯 Was wurde erstellt

### Dateien:
- **`Benutzerverwaltung.app`** - macOS Application Bundle
- **`Benutzerverwaltung.dmg`** - Installer DMG (47.6 MB)

### Features:
- ✅ Native macOS App
- ✅ Benutzer verwalten (UUID, Vorname, Nachname)
- ✅ SQLite Datenbank
- ✅ Automatischer Browser-Start
- ✅ DMG für einfache Installation

## 🚀 Installation (für Endnutzer)

1. **DMG öffnen:** Doppelklick auf `Benutzerverwaltung.dmg`
2. **App installieren:** `Benutzerverwaltung.app` in den `Applications` Ordner ziehen
3. **App starten:** Doppelklick auf die App in Applications
4. **Browser öffnet automatisch** mit der Anwendung

## 🛠️ Build-Prozess (für Entwickler)

### Voraussetzungen:
```bash
pip install Flask Flask-CORS PyInstaller
```

### macOS App erstellen:
```bash
python build_macos.py
```

### DMG Package erstellen:
```bash
python create_dmg.py
```

### Oder beides in einem Schritt:
```bash
python build_macos.py && python create_dmg.py
```

## 📱 Nutzung

1. **App starten:** Doppelklick auf `Benutzerverwaltung.app`
2. **Browser öffnet automatisch:** `http://127.0.0.1:5000`
3. **Funktionen:**
   - Benutzer hinzufügen (Vorname + Nachname)
   - Benutzer bearbeiten
   - Benutzer löschen
   - Alle Änderungen werden in SQLite gespeichert

## 🗄️ Datenspeicherung

- SQLite Datenbank wird automatisch erstellt
- Speicherort: Im gleichen Verzeichnis wie die App
- Daten bleiben nach App-Neustart erhalten

## 🔧 Technische Details

- **Framework:** Flask + SQLite
- **Frontend:** HTML/CSS/JavaScript (eingebettet)
- **Packaging:** PyInstaller für macOS
- **DMG Creation:** hdiutil
- **Architektur:** ARM64 (Apple Silicon)
- **Kompatibilität:** macOS 11.1+

## 🐛 Fehlerbehebung

### App startet nicht:
```bash
# Im Terminal für Debug-Ausgabe:
./Benutzerverwaltung.app/Contents/MacOS/Benutzerverwaltung
```

### Port bereits belegt:
- Ein anderer Webserver läuft auf Port 5000
- Anderen Service stoppen oder App neustarten

### Datenbank Probleme:
- SQLite Datei löschen für Neustart
- Berechtigungen prüfen

### Gatekeeper Warnung:
```bash
# App erlauben (nach Download):
xattr -dr com.apple.quarantine Benutzerverwaltung.app
```

## 📦 Distribution

### DMG weitergeben:
1. `Benutzerverwaltung.dmg` teilen
2. Empfänger mountet DMG
3. App in Applications ziehen
4. Fertig!

### Größe optimieren:
- Unnötige Python Pakete entfernen
- `--exclude-module` in PyInstaller nutzen

## 🔄 Updates

Für Updates einfach:
1. Neue Version builden
2. Alte App ersetzen
3. Datenbank bleibt erhalten