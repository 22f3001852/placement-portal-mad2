from datetime import datetime
from application.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    fullname = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

    role = db.Column(db.String(), nullable=False, default="student")

    is_blacklisted = db.Column(db.Boolean(), default=False, nullable=False)

