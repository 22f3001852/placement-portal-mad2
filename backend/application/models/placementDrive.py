from application.database import db
from datetime import datetime,timezone

class PlacementDrive(db.Model):
    __tablename__ = "placement_drive"

    id = db.Column(db.Integer(), primary_key=True)

    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"), nullable=False)

    job_title = db.Column(db.String())
    job_description = db.Column(db.Text)
    salary = db.Column(db.Float())
    eligibility_cgpa = db.Column(db.Float())
    eligibility_dept = db.Column(db.String())

    deadline = db.Column(db.DateTime)

    # active / closed
    status = db.Column(db.String(), default="active")

    created_on = db.Column(db.DateTime)

    company = db.relationship("Company", backref="drives")