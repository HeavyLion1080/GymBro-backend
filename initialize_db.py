from config import app, db  # Import your Flask app and database instance
from models import Progress, Exercise  # Import models to create tables

# Run drop_all() and create_all() within the application context
with app.app_context():
    db.drop_all()    # Drop all tables
    db.create_all()  # Create all tables
    print("Database tables dropped and recreated successfully.")
