"""
WSGI entry point for production deployment
Use this with Gunicorn or other WSGI servers
"""

import os
import sys
from pathlib import Path

# Add project directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import the Flask app
from app import app

if __name__ == '__main__':
    app.run()
