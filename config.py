import os

# config.py

# -------------------------------
# MySQL Database Configuration
# -------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # MySQL username
    "password": "subhajit",  # MySQL password
    "database": "court_data" # Database name
}

# -------------------------------
# SQLAlchemy Database URI (ORM)
# -------------------------------
# Format: mysql+mysqlconnector://<user>:<password>@<host>/<database>
SQLALCHEMY_DATABASE_URI = (
    f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
)

# -------------------------------
# Target Court URL
# -------------------------------
COURT_URL = "https://delhihighcourt.nic.in/app/get-case-type-status"

# -------------------------------
# Optional: App Settings
# -------------------------------
DEBUG = True           # Enable debug mode for development
SECRET_KEY = "secret!" # Required if you use Flask sessions
