from application.database import db
from datetime import datetime
from .student import Student
from .placementDrive import PlacementDrive

class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey("student.id"), nullable=False)
    drive_id = db.Column(db.Integer(), db.ForeignKey("placement_drive.id"), nullable=False)

    application_date = db.Column(db.DateTime)

    # applied / shortlisted / selected / rejected
    status = db.Column(db.String(), default="applied")

    student = db.relationship("Student", backref="application")
    drive = db.relationship("PlacementDrive", backref="application")

    # Prevent duplicate applications
    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="unique_application"),
    )
