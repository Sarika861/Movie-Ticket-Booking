"""
Setup script for CineMax Theater Booking System
Initializes the project and creates necessary directories
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_project():
    """Setup the project"""
    print("\n" + "=" * 60)
    print("🎬 CineMax Theater - Project Setup")
    print("=" * 60 + "\n")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ is required")
        sys.exit(1)
    
    print("✅ Python version OK")
    
    # Create necessary directories
    base_dir = Path(__file__).parent
    directories = [
        base_dir / 'data',
        base_dir / 'templates',
        base_dir / 'static',
        base_dir / 'logs'
    ]
    
    print("\n📁 Creating directories...")
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"  ✓ {directory.relative_to(base_dir)}")
    
    # Install requirements
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    env_file = base_dir / '.env'
    if not env_file.exists():
        print("\n⚙️  Creating .env file...")
        env_file.write_text("""# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_TESTING=False

# Security
SECRET_KEY=cinemax_secret_key_2026_development

# Server
HOST=localhost
PORT=5000

# Database
DATABASE_FILE=data/bookings.json

# Logging
LOG_LEVEL=INFO
""")
        print("✓ .env file created")
    
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print("\n🚀 To start the server, run:")
    print("   python app.py")
    print("\n📖 Project structure:")
    print("   - app.py ................ Main Flask application")
    print("   - config.py ............. Configuration settings")
    print("   - database.py ........... Database utilities")
    print("   - templates/ ............ HTML templates")
    print("   - static/ ............... CSS and JavaScript")
    print("   - data/ ................. Persistent data storage")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    setup_project()
