#!/usr/bin/env python3
"""
Startup script for the Art Gallery Problem web application
"""
import os
import sys
import subprocess

def main():
    print("🎨 Art Gallery Problem Solver")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('backend/app.py'):
        print("❌ Error: backend/app.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Install dependencies if requirements.txt exists
    if os.path.exists('requirements.txt'):
        print("📦 Installing dependencies...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                         check=True, capture_output=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("Please install manually: pip install -r requirements.txt")
    
    print("\n🚀 Starting web server...")
    print("📍 Server will be available at: http://localhost:5001")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 40)
    
    # Change to backend directory and run Flask app
    os.chdir('backend')
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
