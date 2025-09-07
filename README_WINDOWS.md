# Benutzerverwaltung - Windows EXE

Eine einfache Benutzerverwaltung mit Flask Backend und eingebettetem Frontend, verpackt als Windows EXE.

## Features

- ✅ Benutzer hinzufügen (UUID, Vorname, Nachname)
- ✅ Benutzer bearbeiten
- ✅ Benutzer löschen
- ✅ SQLite Datenbank
- ✅ Responsive Web-Interface
- ✅ Standalone EXE (keine Installation erforderlich)

## EXE erstellen (für Entwickler)

### Voraussetzungen
- Python 3.8 oder höher
- Windows

### Schritte

1. **Abhängigkeiten installieren:**
   ```cmd
   pip install -r requirements.txt
   ```

2. **EXE erstellen:**
   ```cmd
   python build_exe.py
   ```

   Oder einfach die Batch-Datei ausführen:
   ```cmd
   build_all.bat
   ```

3. **EXE finden:**
   Die fertige EXE befindet sich in: `dist/Benutzerverwaltung.exe`

## Nutzung der EXE

1. **Doppelklick** auf `Benutzerverwaltung.exe`
2. Die Anwendung startet automatisch und öffnet sich im Browser
3. URL: `http://127.0.0.1:5000`

### Funktionen

- **Benutzer hinzufügen:** Vorname und Nachname eingeben, "Hinzufügen" klicken
- **Benutzer bearbeiten:** "Bearbeiten" Button bei einem Benutzer klicken
- **Benutzer löschen:** "Löschen" Button klicken (mit Bestätigung)

### Datenspeicherung

- Die SQLite Datenbank (`users.db`) wird im gleichen Ordner wie die EXE erstellt
- Alle Daten bleiben auch nach Neustart erhalten

### Anwendung beenden

- Browser schließen
- Im Terminal/Command Window `Ctrl+C` drücken
- Oder Fenster schließen

## Technische Details

- **Backend:** Flask mit SQLite
- **Frontend:** HTML/CSS/JavaScript (eingebettet)
- **Packaging:** PyInstaller
- **Datenbank:** SQLite (automatisch erstellt)
- **Port:** 5000 (lokal)

## Fehlerbehebung

### EXE startet nicht
- Antivirus-Software könnte die EXE blockieren
- Als Administrator ausführen
- Windows Defender SmartScreen erlauben

### Browser öffnet sich nicht automatisch
- Manuell http://127.0.0.1:5000 aufrufen
- Firewall könnte Port 5000 blockieren

### Daten gehen verloren
- `users.db` Datei im gleichen Ordner wie die EXE behalten
- Backup der `users.db` Datei erstellen