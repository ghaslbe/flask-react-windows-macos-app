import PyInstaller.__main__
import os
import sys

def build_macos_app_with_tray():
    """Build the macOS application with system tray using PyInstaller"""
    
    # PyInstaller arguments for macOS
    args = [
        'app.py',
        '--onefile',
        '--windowed',  # No terminal window
        '--name=Benutzerverwaltung-Tray',
        '--hidden-import=sqlite3',
        '--hidden-import=uuid',
        '--hidden-import=threading',
        '--hidden-import=webbrowser',
        '--hidden-import=time',
        '--hidden-import=platform',
        '--hidden-import=pystray',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageDraw',
        '--add-data=icons:icons',  # Include icon files
        '--osx-bundle-identifier=com.benutzerverwaltung.tray.app',
        # '--target-arch=universal2',  # Skip universal binary due to conda limitations
    ]
    
    print("Building macOS application with System Tray using PyInstaller...")
    print("Arguments:", args)
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✓ macOS application with System Tray built successfully!")
        print("You can find the application in the 'dist' folder")
        print("File: dist/Benutzerverwaltung-Tray.app")
        print("\nFeatures:")
        print("- System Tray Icon (Rechtsklick für Menü)")
        print("- Browser öffnet automatisch")
        print("- Beenden über Tray-Menü")
        return True
    except Exception as e:
        print(f"❌ Error building macOS application: {e}")
        return False

if __name__ == "__main__":
    success = build_macos_app_with_tray()
    sys.exit(0 if success else 1)