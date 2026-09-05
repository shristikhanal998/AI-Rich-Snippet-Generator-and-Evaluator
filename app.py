# ==========================================
# Rich Struct - Backend Application
# ==========================================

# ---------- Flask ----------
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify
)

# ---------- Database ----------
from flask_sqlalchemy import SQLAlchemy


#----- Environment Variables ----------
from dotenv import load_dotenv

# ---------- Python Built-in Libraries ----------
import os
import json
import logging
import re

from datetime import datetime
# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()


# ==========================================
# Create Flask Application
# ==========================================

app = Flask(__name__)


# ==========================================
# Flask Configuration
# ==========================================

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "rich-struct-development-key"
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(

    "DATABASE_URL",
    "sqlite:///richstruct.db"
)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class TrafficPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hour = db.Column(db.Integer, nullable=False)
    day = db.Column(db.String(20), nullable=False)
    car_count = db.Column(db.Integer, nullable=False)
    bike_count = db.Column(db.Integer, nullable=False)
    bus_count = db.Column(db.Integer, nullable=False)
    truck_count = db.Column(db.Integer, nullable=False)
    total_vehicles = db.Column(db.Integer, nullable=False)
    situation = db.Column(db.String(20), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# ==========================================
# Initialize Database
# ==========================================

db = SQLAlchemy(app)


# ==========================================
# Initialize Login Manager
# ==========================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


# ==========================================
# CSRF Protection
# ==========================================

csrf = CSRFProtect(app)


# ==========================================
# Logging Configuration
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================
#  Landing Page
# ==========================================

@app.route("/")
def landing():
    return render_template("index.html")


# ==========================================
# About Page
# ==========================================

@app.route("/about")
def about():
    return render_template("about.html")


# ==========================================
# Test Route
# ==========================================

@app.route("/landing/test", methods=["GET"])
def test():
    return jsonify({
        "project": "Rich Struct",
        "status": "Backend is working"
    })


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)