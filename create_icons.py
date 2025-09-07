#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw, ImageFont

def create_user_icon(size=32, style="modern"):
    """Create a custom user management icon"""
    # Create image with transparency
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    if style == "modern":
        # Modern flat design
        # Background circle
        margin = 2
        draw.ellipse([margin, margin, size-margin, size-margin], 
                    fill=(0, 123, 255, 255), outline=(0, 86, 179, 255), width=1)
        
        # User icon (simplified person)
        center_x, center_y = size // 2, size // 2
        
        # Head
        head_size = size // 6
        draw.ellipse([center_x - head_size//2, center_y - size//3, 
                     center_x + head_size//2, center_y - size//3 + head_size], 
                    fill=(255, 255, 255, 255))
        
        # Body
        body_width = size // 4
        body_height = size // 4
        draw.rectangle([center_x - body_width//2, center_y - size//8,
                       center_x + body_width//2, center_y + body_height], 
                      fill=(255, 255, 255, 255))
        
    elif style == "database":
        # Database/storage themed
        # Background
        draw.ellipse([2, 2, size-2, size-2], 
                    fill=(40, 167, 69, 255), outline=(33, 136, 56, 255), width=1)
        
        # Database cylinders
        y_positions = [size//4, size//2, 3*size//4]
        for y in y_positions:
            # Cylinder
            draw.rectangle([size//4, y-2, 3*size//4, y+2], fill=(255, 255, 255, 255))
            # Top ellipse
            draw.ellipse([size//4, y-3, 3*size//4, y+1], fill=(255, 255, 255, 255))
    
    elif style == "gear":
        # Settings/management themed
        # Background
        draw.ellipse([2, 2, size-2, size-2], 
                    fill=(108, 117, 125, 255), outline=(73, 80, 87, 255), width=1)
        
        # Gear shape (simplified)
        center = size // 2
        # Central circle
        draw.ellipse([center-4, center-4, center+4, center+4], 
                    fill=(255, 255, 255, 255))
        # Gear teeth (simplified as rectangles)
        for angle in range(0, 360, 45):
            if angle % 90 == 0:  # Only 4 teeth
                if angle == 0:    # Right
                    draw.rectangle([center+3, center-1, center+6, center+1], 
                                 fill=(255, 255, 255, 255))
                elif angle == 90: # Bottom
                    draw.rectangle([center-1, center+3, center+1, center+6], 
                                 fill=(255, 255, 255, 255))
                elif angle == 180: # Left
                    draw.rectangle([center-6, center-1, center-3, center+1], 
                                 fill=(255, 255, 255, 255))
                elif angle == 270: # Top
                    draw.rectangle([center-1, center-6, center+1, center-3], 
                                 fill=(255, 255, 255, 255))
    
    return image

def create_all_icons():
    """Create all needed icon variations"""
    
    if not os.path.exists('icons'):
        os.makedirs('icons')
    
    styles = [
        ("modern", "Moderne Benutzer-Darstellung"),
        ("database", "Datenbank-Thema (grün)"), 
        ("gear", "Verwaltung/Einstellungen (grau)")
    ]
    
    sizes = [16, 24, 32, 48, 64]
    
    print("🎨 Erstelle Icon-Varianten...")
    
    for style, description in styles:
        print(f"\n📁 {description}:")
        
        # Create different sizes
        for size in sizes:
            icon = create_user_icon(size, style)
            filename = f"icons/icon_{style}_{size}x{size}.png"
            icon.save(filename, "PNG")
            print(f"   ✓ {filename}")
        
        # Create ICO file for Windows (multiple sizes in one file)
        ico_images = [create_user_icon(size, style) for size in [16, 32, 48]]
        ico_filename = f"icons/icon_{style}.ico"
        ico_images[0].save(ico_filename, "ICO", sizes=[(16,16), (32,32), (48,48)], 
                          append_images=ico_images[1:])
        print(f"   ✓ {ico_filename} (Windows)")

def create_example_readme():
    """Create documentation for the icons"""
    content = """# 🎨 Icon-Dateien für Benutzerverwaltung

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
"""
    
    with open('icons/README.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📖 icons/README.md erstellt")

if __name__ == "__main__":
    print("=" * 50)
    print("🎨 Icon-Generator für Benutzerverwaltung")
    print("=" * 50)
    
    try:
        create_all_icons()
        create_example_readme()
        
        print("\n" + "=" * 50)
        print("✅ Alle Icons erfolgreich erstellt!")
        print("\n📁 Verfügbare Styles:")
        print("   • icon_modern.*    - Blau, benutzerfreundlich")
        print("   • icon_database.*  - Grün, datenorientiert")  
        print("   • icon_gear.*      - Grau, professionell")
        print("\n🔧 Nächste Schritte:")
        print("   1. Icon auswählen: icons/icon_modern_32x32.png")
        print("   2. In app_with_tray.py einbinden")
        print("   3. App neu builden")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        print("Stellen Sie sicher, dass Pillow installiert ist: pip install Pillow")