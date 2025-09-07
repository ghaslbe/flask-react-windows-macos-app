# 🎨 Icon-Dateien für Benutzerverwaltung

## 📁 Verfügbare Icons

### 1. Modern (Blau) - `icon_modern`
- 👤 Stilisierte Person auf blauem Hintergrund
- Moderne, freundliche Darstellung
- **Empfohlen für Standard-Nutzung**

### 2. Database (Grün) - `icon_database`  
- 💾 Datenbank-Zylinder Darstellung
- Betont Datenspeicherung
- Gut für technische Nutzer

### 3. Gear (Grau) - `icon_gear`
- ⚙️ Zahnrad für Verwaltung/Einstellungen
- Professionell und neutral
- Gut für Enterprise-Umgebung

## 📏 Verfügbare Größen
- 16x16, 24x24, 32x32, 48x48, 64x64 (PNG)
- Multi-Size ICO-Dateien für Windows

## 🔧 Verwendung

### In der Anwendung:
```python
# PNG verwenden (empfohlen):
icon_path = "icons/icon_modern_32x32.png"

# ICO für Windows:
icon_path = "icons/icon_modern.ico"
```

### Eigene Icons hinzufügen:
1. **PNG-Datei erstellen** (32x32 Pixel optimal)
2. **In icons/ Ordner speichern**
3. **In app_with_tray.py einbinden**

### Bestes Icon auswählen:
- **Standard-App:** `icon_modern` (freundlich)
- **Business-App:** `icon_gear` (professionell)  
- **Daten-App:** `icon_database` (funktional)
