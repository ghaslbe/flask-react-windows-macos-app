#!/usr/bin/env python3

import os
import subprocess
import shutil
import sys

def create_dmg():
    """Create a DMG file for macOS distribution"""
    
    app_name = "Benutzerverwaltung"
    app_path = f"dist/{app_name}.app"
    dmg_name = f"{app_name}.dmg"
    volume_name = "Benutzerverwaltung Installer"
    
    # Check if app exists
    if not os.path.exists(app_path):
        print(f"❌ Application not found: {app_path}")
        print("Please run build_macos.py first")
        return False
    
    # Clean up old DMG
    if os.path.exists(dmg_name):
        os.remove(dmg_name)
        print(f"🗑️  Removed old {dmg_name}")
    
    # Create temporary directory for DMG contents
    temp_dir = "dmg_temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        # Copy app to temp directory
        print("📦 Copying application to DMG folder...")
        shutil.copytree(app_path, f"{temp_dir}/{app_name}.app")
        
        # Create Applications symlink
        print("🔗 Creating Applications symlink...")
        os.symlink("/Applications", f"{temp_dir}/Applications")
        
        # Create README file for DMG
        readme_content = """# Benutzerverwaltung für macOS

## Installation
1. Ziehen Sie "Benutzerverwaltung.app" in den Applications-Ordner
2. Doppelklick auf die App zum Starten
3. Die Anwendung öffnet sich automatisch im Browser

## Verwendung
- **Benutzer hinzufügen:** Vorname und Nachname eingeben
- **Benutzer bearbeiten:** "Bearbeiten" Button klicken
- **Benutzer löschen:** "Löschen" Button klicken

## Datenspeicherung
Die SQLite-Datenbank wird automatisch im Home-Verzeichnis erstellt.

## Support
Bei Problemen die Anwendung aus dem Terminal starten für Debug-Ausgaben.
"""
        
        with open(f"{temp_dir}/README.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        # Calculate size for DMG
        print("📏 Calculating DMG size...")
        size_result = subprocess.run(['du', '-sk', temp_dir], capture_output=True, text=True)
        if size_result.returncode == 0:
            size_kb = int(size_result.stdout.split()[0])
            # Add 50% margin for DMG overhead
            dmg_size_kb = int(size_kb * 1.5)
        else:
            dmg_size_kb = 200000  # 200MB fallback
        
        print(f"💾 Creating DMG ({dmg_size_kb}KB)...")
        
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
            # Get DMG info
            dmg_size = os.path.getsize(dmg_name)
            dmg_size_mb = dmg_size / (1024 * 1024)
            
            print(f"✅ DMG created successfully!")
            print(f"📦 File: {dmg_name}")
            print(f"💾 Size: {dmg_size_mb:.1f} MB")
            
            # Verify DMG
            print("🔍 Verifying DMG...")
            verify_result = subprocess.run(['hdiutil', 'verify', dmg_name], 
                                         capture_output=True, text=True)
            if verify_result.returncode == 0:
                print("✅ DMG verification successful!")
            else:
                print("⚠️  DMG verification failed but file was created")
            
            return True
        else:
            print(f"❌ Failed to create DMG:")
            print(f"Error: {result.stderr}")
            return False
            
    finally:
        # Clean up temp directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🧹 Cleaned up temporary files")

def main():
    print("=" * 50)
    print("Creating macOS DMG Package")
    print("=" * 50)
    
    if not shutil.which('hdiutil'):
        print("❌ hdiutil not found. This script requires macOS.")
        sys.exit(1)
    
    success = create_dmg()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 DMG creation completed successfully!")
        print("\nTo distribute:")
        print("1. Test the DMG by mounting it")
        print("2. Share the .dmg file with users")
        print("3. Users can drag the app to Applications")
    else:
        print("❌ DMG creation failed")
    print("=" * 50)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()