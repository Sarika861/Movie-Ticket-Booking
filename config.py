"""
Configuration settings for CineMax Theater Booking System
Production-ready Full-Stack Project with SQLAlchemy & Stripe
"""

import os
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).parent.absolute()

# Flask Configuration
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
TESTING = os.environ.get('FLASK_TESTING', 'False').lower() == 'true'
SECRET_KEY = os.environ.get('SECRET_KEY', 'cinemax_secret_key_2026_production_change_me')

# Server Configuration
HOST = os.environ.get('HOST', 'localhost')
PORT = int(os.environ.get('PORT', 5000))
THREADED = True

# Directories
TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
DATA_DIR = BASE_DIR / 'data'
MIGRATIONS_DIR = BASE_DIR / 'migrations'

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
MIGRATIONS_DIR.mkdir(exist_ok=True)

# Database Configuration - SQLAlchemy with SQLite
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    f'sqlite:///{DATA_DIR / "cinemax.db"}'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = DEBUG  # Log SQL queries in debug mode

# Theater Configuration
THEATER_NAME = "CineMax Theater"
MAX_SCREENS = 10
DEFAULT_ROWS = 8
DEFAULT_SEATS_PER_ROW = 12

# Session Configuration
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Payment Configuration - Stripe
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_your_test_key_here')
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', 'pk_test_your_test_key_here')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_test_key_here')

# Payment Settings
PAYMENT_CURRENCY = 'usd'
PAYMENT_DESCRIPTION_FORMAT = 'CineMax Theater - {movie_title} - {seats_count} seats'
PAYMENT_PROCESSING_FEE_PERCENTAGE = 2.9  # 2.9% + $0.30 per transaction
PAYMENT_PROCESSING_FEE_FIXED = 0.30

# Logging Configuration
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = DATA_DIR / 'app.log'

# Email Configuration (for payment confirmations, optional)
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@cinemax.com')
