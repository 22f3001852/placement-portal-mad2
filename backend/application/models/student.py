from application.database import db
from .user import User

class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))

    fullname = db.Column(db.String())
    department = db.Column(db.String(), nullable=False)
    cgpa = db.Column(db.Float(), nullable=False)

    year = db.Column(db.Integer())

    resume = db.Column(db.LargeBinary)
    
    user = db.relationship("User", backref="student", lazy=True)