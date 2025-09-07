#!/usr/bin/env python3

import os
import subprocess
import shutil
import sys

def create_tray_dmg():
    """Create a DMG file for the Tray version"""
    
    app_name = "Benutzerverwaltung-Tray"
    app_path = f"dist/{app_name}.app"
    dmg_name = f"{app_name}.dmg"
    volume_name = "Benutzerverwaltung Tray Installer"
    
    # Check if app exists
    if not os.path.exists(app_path):
        print(f"❌ Application not found: {app_path}")
        print("Please run build_macos_tray.py first")
        return False
    
    # Clean up old DMG
    if os.path.exists(dmg_name):
        os.remove(dmg_name)
        print(f"🗑️  Removed old {dmg_name}")
    
    # Create temporary directory for DMG contents
    temp_dir = "dmg_temp_tray"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        # Copy app to temp directory
        print("📦 Copying Tray application to DMG folder...")
        shutil.copytree(app_path, f"{temp_dir}/{app_name}.app")
        
        # Create Applications symlink
        print("🔗 Creating Applications symlink...")
        os.symlink("/Applications", f"{temp_dir}/Applications")
        
        # Create README file for Tray DMG
        readme_content = """# Benutzerverwaltung Tray für macOS

## ✨ Neue Features der Tray-Version
- 📍 **System Tray Icon** in der macOS Menüleiste
- 🖱️ **Rechtsklick-Menü** für einfache Steuerung
- 🚀 **Sichtbare App-Kontrolle** (kein versteckter Prozess)
- 📁 **Direkter Zugriff** zum Datenordner

## 🏗️ Installation
1. Ziehen Sie "Benutzerverwaltung-Tray.app" in den Applications-Ordner
2. Doppelklick auf die App zum Starten
3. **Tray-Icon** erscheint oben rechts in der Menüleiste
4. Browser öffnet automatisch mit der Anwendung

## 🎛️ Bedienung
- **App öffnen:** Rechtsklick auf Tray-Icon → "Benutzerverwaltung öffnen"
- **Datenordner:** Rechtsklick → "Datenbank-Ordner"  
- **Beenden:** Rechtsklick → "Beenden"

## 📁 Datenspeicherung
SQLite-Datenbank: ~/Documents/Benutzerverwaltung/users.db

## 🆚 Unterschied zur Standard-Version
- **Standard:** Läuft unsichtbar im Hintergrund
- **Tray:** Sichtbares Icon mit Kontrollmöglichkeiten
"""
        
        with open(f"{temp_dir}/README_TRAY.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        # Calculate size for DMG
        print("📏 Calculating DMG size...")
        size_result = subprocess.run(['du', '-sk', temp_dir], capture_output=True, text=True)
        if size_result.returncode == 0:
            size_kb = int(size_result.stdout.split()[0])
            dmg_size_kb = int(size_kb * 1.5)
        else:
            dmg_size_kb = 200000
        
        print(f"💾 Creating Tray DMG ({dmg_size_kb}KB)...")
        
        # Create DMG
        cmd = [
            'hdiutil', 'create',
            '-size', f'{dmg_size_kb}k',
            '-volname', volume_name,
            '-srcfolder', temp_dir,
            '-fs', 'HFS+',
            '-format', 'UDZO',
            dmg_name
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            dmg_size = os.path.getsize(dmg_name)
            dmg_size_mb = dmg_size / (1024 * 1024)
            
            print(f"✅ Tray DMG created successfully!")
            print(f"📦 File: {dmg_name}")
            print(f"💾 Size: {dmg_size_mb:.1f} MB")
            
            return True
        else:
            print(f"❌ Failed to create DMG:")
            print(f"Error: {result.stderr}")
            return False
            
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    print("=" * 50)
    print("Creating macOS Tray DMG Package")
    print("=" * 50)
    
    success = create_tray_dmg()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Tray DMG creation completed!")
        print("\n📦 Ready for GitHub Release:")
        print("   • Benutzerverwaltung-Tray.dmg (macOS Tray Version)")
    else:
        print("❌ Tray DMG creation failed")
    print("=" * 50)
    
    sys.exit(0 if success else 1)