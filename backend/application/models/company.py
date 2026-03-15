from application.database import db
from .user import User

class Company(db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)

    company_name = db.Column(db.String())
    hr_contact = db.Column(db.String())
    website = db.Column(db.String())
    location = db.Column(db.String())

    #pending/approved
    approval_status = db.Column(db.String(), default="pending")

    user = db.relationship("User", backref="company")

