import PyInstaller.__main__
import os
import sys

def build_macos_app():
    """Build the macOS application using PyInstaller"""
    
    # PyInstaller arguments for macOS
    args = [
        'app_exe.py',
        '--onefile',
        '--windowed',  # No terminal window
        '--name=Benutzerverwaltung',
        '--hidden-import=sqlite3',
        '--hidden-import=uuid',
        '--hidden-import=threading',
        '--hidden-import=webbrowser',
        '--hidden-import=time',
        '--hidden-import=platform',
        '--osx-bundle-identifier=com.benutzerverwaltung.app',
        # '--target-arch=universal2',  # Skip universal binary due to conda limitations
    ]
    
    print("Building macOS application with PyInstaller...")
    print("Arguments:", args)
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✓ macOS application built successfully!")
        print("You can find the application in the 'dist' folder")
        print("File: dist/Benutzerverwaltung.app")
        return True
    except Exception as e:
        print(f"❌ Error building macOS application: {e}")
        return False

if __name__ == "__main__":
    success = build_macos_app()
    sys.exit(0 if success else 1)