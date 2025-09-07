import PyInstaller.__main__
import os
import sys

def build_windows_exe_with_tray():
    """Build the Windows executable with system tray using PyInstaller"""
    
    # PyInstaller arguments
    args = [
        'app_with_tray.py',
        '--onefile',
        '--windowed',  # No console window
        '--name=Benutzerverwaltung-Tray',
        '--icon=icons/icon_modern.ico' if os.path.exists('icons/icon_modern.ico') else '--icon=NONE',
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
        '--add-data=icons;icons'  # Include icon files for Windows
    ]
    
    # Remove empty args
    args = [arg for arg in args if arg]
    
    print("Building Windows executable with System Tray using PyInstaller...")
    print("Arguments:", args)
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✓ Windows executable with System Tray built successfully!")
        print("You can find the executable in the 'dist' folder")
        print("File: dist/Benutzerverwaltung-Tray.exe")
        print("\nFeatures:")
        print("- System Tray Icon (Rechtsklick für Menü)")
        print("- Browser öffnet automatisch")
        print("- Beenden über Tray-Menü")
        return True
    except Exception as e:
        print(f"❌ Error building executable: {e}")
        return False

if __name__ == "__main__":
    success = build_windows_exe_with_tray()
    sys.exit(0 if success else 1)