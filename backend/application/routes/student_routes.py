from flask import Blueprint, request, jsonify, abort, send_from_directory
from flask_jwt_extended import create_access_token,current_user,jwt_required
from datetime import datetime,timezone
from application.utils.decorator import role_required
from application.database import db
from application.models.user import User
from application.models.student import Student
from application.models.company import Company
from application.models.placementDrive import PlacementDrive
from application.models.application import Application

from celery.result import AsyncResult
from application.tasks import daily_deadline_reminder,export_application_history

from application.cache_init import cache

student_bp = Blueprint('student', __name__)

@student_bp.route("/apply/<int:drive_id>", methods=["POST"])
@jwt_required()
@role_required("student")
def apply_drive(drive_id):

    if request.method =='POST':
        if current_user.is_blacklisted == True:
                return jsonify(message="Blacklisted Student Can Not Apply for Any Drive"),403
        
        student = Student.query.filter_by(user_id=current_user.id).first()

        existing_student = Application.query.filter_by(student_id=student.id,drive_id=drive_id).first()

        if existing_student:
            return jsonify({"message":"Already applied"}),400
        
        application_date = datetime.now(timezone.utc)

        new_application = Application(student_id=student.id,drive_id=drive_id,status="applied",application_date=application_date)

        db.session.add(new_application)
        db.session.commit()

        return jsonify({"message":"Application submitted successfully"})


@student_bp.route("/company-drives/<int:company_id>", methods=["GET"])
@cache.cached(timeout=10)
@jwt_required()
@role_required("student")
def companyDrives(company_id):

    company = Company.query.get(company_id)

    if not company:
        abort(404, description="Company not found")

    drives = PlacementDrive.query.filter_by(company_id=company_id,status="active").all()

    drives_data = []

    for drive in drives:
        drives_data.append({
            "id": drive.id,
            "job_title": drive.job_title,
            "salary": drive.salary,
            "deadline": drive.deadline
        })

    return jsonify({
        "company_name": company.company_name,
        "drives": drives_data
    })

@student_bp.route("/history", methods=["GET"])
@cache.cached(timeout=30)
@jwt_required()
@role_required("student")
def student_history():

    if current_user.is_blacklisted:
        return jsonify({"message": "Blacklisted user cannot access history"}), 403

    student = Student.query.filter_by(user_id=current_user.id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    applications = (
        Application.query
        .filter(Application.student_id == student.id)
        .all()
    )

    history = []

    for app in applications:
        drive = app.drive

        history.append({
            "drive_id": drive.id,
            "job_title": drive.job_title,
            "company_name":drive.company.company_name,
            "salary": float(drive.salary),
            "status": app.status
        })

    return jsonify({
        "student": {
            "id":student.id,
            "name": student.fullname,
            "department": student.department
        },
        "applications": history
    }), 200


@student_bp.route("/export_csv/<int:student_id>")
def export(student_id):
    task = export_application_history.delay(student_id)
    return {
        "task_id": task.id
    }

@student_bp.route("/csv_result/<task_id>")
def csv_result(task_id):
    res = AsyncResult(task_id)

    if not res.ready():
        return jsonify({"status": "processing"})

    if res.failed():
        return jsonify({"status": "failed"})

    return send_from_directory('static', res.result)

@student_bp.route('/send_mail')
def send_mail():
    report = daily_deadline_reminder.delay()
    return {
        "message": report.result
    }