from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Use environment variables for configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("FLASK_APP_SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("FLASK_APP_SQLALCHEMY_TRACK_MODIFICATIONS") == "True"

db = SQLAlchemy(app)
