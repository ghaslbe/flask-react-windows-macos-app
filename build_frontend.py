import subprocess
import sys
import os

def build_frontend():
    """Build the React frontend"""
    print("Installing npm dependencies...")
    try:
        subprocess.run(['npm', 'install'], check=True, cwd=os.getcwd())
        print("✓ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    
    print("Building React frontend...")
    try:
        subprocess.run(['npm', 'run', 'build'], check=True, cwd=os.getcwd())
        print("✓ Frontend built successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to build frontend")
        return False

if __name__ == "__main__":
    success = build_frontend()
    sys.exit(0 if success else 1)