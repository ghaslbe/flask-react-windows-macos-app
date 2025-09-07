import PyInstaller.__main__
import os
import sys

def build_exe():
    """Build the executable using PyInstaller"""
    
    # PyInstaller arguments
    args = [
        'app_exe.py',
        '--onefile',
        '--windowed',  # No console window
        '--name=Benutzerverwaltung',
        '--icon=icons/icon_modern.ico' if os.path.exists('icons/icon_modern.ico') else '--icon=NONE',
        '--add-data=users.db;.' if os.path.exists('users.db') else '',
        '--hidden-import=sqlite3',
        '--hidden-import=uuid',
        '--hidden-import=threading',
        '--hidden-import=webbrowser',
        '--hidden-import=time',
        '--hidden-import=platform'
    ]
    
    # Remove empty args
    args = [arg for arg in args if arg]
    
    print("Building executable with PyInstaller...")
    print("Arguments:", args)
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✓ Executable built successfully!")
        print("You can find the executable in the 'dist' folder")
        print("File: dist/Benutzerverwaltung.exe")
        return True
    except Exception as e:
        print(f"❌ Error building executable: {e}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)