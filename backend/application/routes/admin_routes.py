from flask import Blueprint, request, jsonify,abort
from flask_jwt_extended import current_user


from application.models.user import User
from application.models.student import Student
from application.models.company import Company
from application.models.placementDrive import PlacementDrive
from application.models.application import Application

from flask_jwt_extended import create_access_token,current_user,jwt_required
from application.utils.decorator import role_required
from application.database import db


from celery.result import AsyncResult
from application.tasks import monthly_activity_report

from application.cache_init import cache

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/users", methods=["GET","POST"])
@jwt_required()
@role_required("admin")
def adminUsers():

    requested_companies = Company.query.filter_by(approval_status="pending").all()

    students = Student.query.join(Student.user).filter(User.is_blacklisted == False).all()
    blacklisted_students = Student.query.join(Student.user).filter(User.is_blacklisted == True).all()
    companies = Company.query.join(Company.user).filter(Company.approval_status == "approved",User.is_blacklisted == False).all()
    blacklisted_companies = Company.query.join(Company.user).filter(Company.approval_status == "approved",User.is_blacklisted == True).all()

    def serialize_company(company):
        return {
            "id": company.id,
            "user_id": company.user_id,
            "company_code": f"COMP{company.id:03d}",
            "name": company.company_name,
            "email": company.user.username,
            "hr_contact": company.hr_contact,
        }

    def serialize_student(student):
        return {
            "id": student.id,
            "user_id": student.user_id,
            "student_code": f"ST{student.id:03d}",
            "name": student.fullname,
            "department": student.department,
            "cgpa": student.cgpa
        }

    return jsonify({
        "requested_companies":[serialize_company(each_company) for each_company in requested_companies],
        "students":[serialize_student(each_student) for each_student in students],
        "companies":[serialize_company(each_company) for each_company in companies],
        "blacklisted_students":[serialize_student(each_student) for each_student in blacklisted_students],
        "blacklisted_companies":[serialize_company(each_company) for each_company in blacklisted_companies]
    }),200

@admin_bp.route("/blacklist/<int:user_id>",methods=['POST'])
@jwt_required()
@role_required("admin")
def blacklist(user_id):
    this_user = User.query.get_or_404(user_id)

    if this_user.is_blacklisted:
        abort(400, description="User already blacklisted")

    if this_user.role == "student":
        student = Student.query.filter_by(user_id=user_id).first()

        if student:
            for app in student.application:
                if app.status not in ["selected", "rejected"]:
                    app.status = "rejected"

        this_user.is_blacklisted = True
        db.session.commit()

    elif this_user.role == "company":
        company = Company.query.filter_by(user_id=user_id).first()

        if company:
            # Reject related applications
            applications = Application.query.join(PlacementDrive).filter(PlacementDrive.company_id == company.id).all()

            for app in applications:
                if app.status not in ["selected", "rejected"]:
                    app.status = "rejected"

            # Close related drives
            drives = PlacementDrive.query.filter_by(company_id=company.id,status="active").all()

            for drive in drives:
                drive.status = "closed"

        this_user.is_blacklisted = True
        db.session.commit()
    

    return jsonify({
        "message": f"{this_user.fullname} blacklisted successfully"
        })


@admin_bp.route("/permit-user/<int:user_id>", methods=["POST"])
@jwt_required()
@role_required("admin")
def permit_user(user_id):

    user = User.query.get_or_404(user_id)

    if not user.is_blacklisted:
        return jsonify({"message":"User is already permitted"}),400

    user.is_blacklisted = False

    db.session.commit()

    return jsonify({
        "message":"User permitted successfully"
    }),200


@admin_bp.route("/drive/close/<int:drive_id>", methods=["POST"])
@role_required("admin")
def closeDrive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)

    # if current_user.is_blacklisted:
    #     return jsonify(message="Blacklisted company cannot close drives"), 403

    # if drive.company.user_id != current_user.id:
    #     return jsonify(message="Unauthorized action"), 403

    if drive.status == "closed":
        return jsonify(message="Drive already closed"), 400

    drive.status = "closed"
    db.session.commit()

    return jsonify(message= "Drive closed successfully"), 200



@admin_bp.route("/drives", methods=["GET"])
@cache.cached(timeout=60)
@jwt_required()
@role_required("admin")
def adminDrives():

    # student applications
    applications = Application.query.all()

    # ongoing drives
    drives = PlacementDrive.query.filter_by(status="active").all()

    def serialize_application(app):
        return {
            "id": app.id,
            "student_name": app.student.fullname,
            "drive_title": app.drive.job_title,
            "status": app.status,
            "applied_on":app.application_date
        }

    def serialize_drive(drive):
        return {
            "id": drive.id,
            "drive_code": f"DRV{drive.id:03d}",
            "job_title": drive.job_title,
            "deadline":drive.deadline,
            "company_name": drive.company.company_name
        }

    return jsonify({
        "applications":[serialize_application(a) for a in applications],
        "drives":[serialize_drive(d) for d in drives]
    }),200



@admin_bp.route("/action/<int:user_id>", methods=["POST"])
@jwt_required()
@role_required("admin")
def companyAction(user_id):
    company = Company.query.filter_by(user_id=user_id).first_or_404()
    action = request.json.get("action")
    if action == "approve":
        if company.approval_status == "approved":
            return jsonify({"message": "Company already approved"}), 400
        company.approval_status = "approved"
        message = f"{company.company_name} approved successfully"
    elif action == "reject":
        company.approval_status = "rejected"
        message = f"{company.company_name} rejected successfully"
    else:
        return jsonify({"message": "Invalid action"}), 400
    db.session.commit()

    return jsonify({
        "message": message
    }), 200


@admin_bp.route('/send_mail')
def send_mail():
    report = monthly_activity_report.delay()
    return {
        "message": report.result
        # "message": "Task started",
        # "task_id": report.id
    }

