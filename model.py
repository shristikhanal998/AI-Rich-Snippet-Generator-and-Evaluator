from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import datetime # Initialize the db object db = SQLAlchemy() class User(db.Model, UserMixin):
# Initialize the db object
db = SQLAlchemy() 
class User(db.Model, UserMixin):
 
    # Primary ID for each user
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Unique username for login
    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    # Unique email for registration
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    # Encrypted password
    password_hash = db.Column(
        db.String(256),
        nullable=False
    )

    # Date of registration
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def set_password(self, password):
        """Convert plain password into a secure hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check entered password against stored hash."""
        return check_password_hash(
            self.password_hash,
            password
        )

    def __repr__(self):
        return f"<User {self.username}>"