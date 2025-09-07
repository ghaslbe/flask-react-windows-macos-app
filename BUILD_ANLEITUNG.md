# 🚀 Build-Anleitung für Benutzerverwaltung

Eine komplette Anleitung zum Erstellen der Standalone-Anwendung für Windows und macOS.

## 📋 Voraussetzungen

### Für beide Plattformen:
- **Python 3.8 oder höher**
- **Git** (optional, für Versionskontrolle)

### Prüfen der Python-Version:
```bash
python --version
# oder
python3 --version
```

## 🪟 Windows Build

### 1. Abhängigkeiten installieren
```cmd
pip install -r requirements.txt
```

### 2. EXE erstellen
**Option A - Automatisch (empfohlen):**
```cmd
build_all.bat
```

**Option B - Manuell:**
```cmd
python build_exe.py
```

### 3. Ergebnis finden
```
dist/Benutzerverwaltung.exe
```

### 4. Testen
```cmd
# EXE ausführen
dist\Benutzerverwaltung.exe
```

---

## 🍎 macOS Build

### 1. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 2. App erstellen
```bash
python build_macos.py
```

### 3. DMG erstellen (optional, für Distribution)
```bash
python create_dmg.py
```

### 4. Ergebnis finden
```
dist/Benutzerverwaltung.app    # macOS App
Benutzerverwaltung.dmg         # Installer DMG
```

### 5. Testen
```bash
# App ausführen
open dist/Benutzerverwaltung.app
```

---

## 🔧 Vollständiger Build-Prozess

### Windows (kompletter Prozess):
```cmd
# 1. Abhängigkeiten installieren
pip install -r requirements.txt

# 2. Anwendung testen (optional)
python test_app.py

# 3. EXE erstellen
python build_exe.py

# 4. Fertig!
echo "EXE verfügbar in: dist\Benutzerverwaltung.exe"
```

### macOS (kompletter Prozess):
```bash
# 1. Abhängigkeiten installieren
pip install -r requirements.txt

# 2. Anwendung testen (optional)
python test_app.py

# 3. App erstellen
python build_macos.py

# 4. DMG erstellen
python create_dmg.py

# 5. Fertig!
echo "App: dist/Benutzerverwaltung.app"
echo "DMG: Benutzerverwaltung.dmg"
```

---

## 📁 Dateistruktur nach dem Build

```
projekt-ordner/
├── app_exe.py              # Hauptanwendung
├── requirements.txt        # Python-Abhängigkeiten
├── build_exe.py           # Windows Build-Script
├── build_macos.py         # macOS Build-Script
├── create_dmg.py          # DMG-Ersteller
├── build_all.bat          # Windows Auto-Build
├── test_app.py            # Test-Script
├── dist/                  # Build-Ergebnisse
│   ├── Benutzerverwaltung.exe    # Windows (nur auf Windows)
│   └── Benutzerverwaltung.app    # macOS (nur auf macOS)
└── Benutzerverwaltung.dmg # macOS Installer (nur auf macOS)
```

---

## 🎯 Distribution

### Windows:
1. **EXE verteilen:** `dist/Benutzerverwaltung.exe`
2. **Benutzer:** Doppelklick zum Starten
3. **Daten:** `%USERPROFILE%\Documents\Benutzerverwaltung\`

### macOS:
1. **DMG verteilen:** `Benutzerverwaltung.dmg`
2. **Installation:** DMG mounten → App zu Applications ziehen
3. **Daten:** `~/Documents/Benutzerverwaltung/`

---

## 🐛 Fehlerbehebung

### Allgemeine Probleme:

**PyInstaller fehlt:**
```bash
pip install PyInstaller
```

**Modul nicht gefunden:**
```bash
pip install Flask Flask-CORS
```

### Windows-spezifisch:

**"python" nicht erkannt:**
```cmd
# Python über Microsoft Store installieren
# oder python.exe verwenden
python.exe build_exe.py
```

**Antivirus blockiert EXE:**
- EXE temporär aus Antivirus-Scan ausschließen
- Windows Defender SmartScreen erlauben

### macOS-spezifisch:

**"App beschädigt" Meldung:**
```bash
# Quarantäne entfernen
xattr -dr com.apple.quarantine dist/Benutzerverwaltung.app
```

**hdiutil nicht gefunden:**
- DMG-Erstellung nur auf macOS verfügbar
- App direkt ohne DMG verteilen

---

## ✅ Erfolgreich gebaut - Was nun?

### Testen:
1. **App starten** - sollte Browser automatisch öffnen
2. **Benutzer hinzufügen** - Vorname + Nachname
3. **Funktionen testen** - Bearbeiten, Löschen
4. **App beenden** - Daten sollten erhalten bleiben

### Verteilen:
1. **Windows:** EXE-Datei teilen
2. **macOS:** DMG-Datei teilen
3. **Dokumentation:** Diese Anleitung mitgeben

### Datenbank-Speicherort:
- **Windows:** `C:\Users\[Name]\Documents\Benutzerverwaltung\`
- **macOS:** `/Users/[Name]/Documents/Benutzerverwaltung/`

---

## 🔄 Updates erstellen

Für neue Versionen:
1. Code anpassen
2. Build-Prozess wiederholen
3. Neue EXE/DMG verteilen
4. **Datenbank bleibt erhalten!**

---

## 📞 Support

Bei Problemen:
1. **Terminal-Ausgabe prüfen** (bei Fehlern)
2. **Datenbankpfad prüfen** (wird beim Start angezeigt)
3. **Port 5000 frei** (andere Webserver beenden)
4. **Firewall-Einstellungen** prüfen