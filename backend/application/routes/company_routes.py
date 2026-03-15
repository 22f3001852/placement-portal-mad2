from flask import Blueprint, request, jsonify,abort
from flask_jwt_extended import current_user
from datetime import datetime
from datetime import datetime,timezone
import pytz
# import io
from application.models.user import User
from application.models.student import Student
from application.models.company import Company
from application.models.placementDrive import PlacementDrive
from application.models.application import Application
from flask_jwt_extended import create_access_token,current_user,jwt_required
from application.utils.decorator import role_required
from application.database import db

company_bp = Blueprint('company', __name__)


IST = pytz.timezone('Asia/Kolkata')
# ist_created_time = created_at.astimezone(IST)
# readable_ist_created_time = ist_created_time.strftime("%d/%m/%Y %H:%M")

@company_bp.route('/create-drive',methods=['POST'])
@jwt_required()
@role_required('company')
def createDrive():
    if request.method == 'POST':
        if current_user.is_blacklisted == True:
            return jsonify(message="Blacklisted Company can not create any drive"),403
        
        job_title = request.json.get("job_title")
        job_description = request.json.get("job_description")
        salary = request.json.get("salary")
        eligibility_cgpa = request.json.get("eligibility_cgpa")
        eligibility_dept = request.json.get("eligibility_dept")

        deadline = request.json.get("deadline")
        deadline = datetime.strptime(deadline, "%Y-%m-%d")
        deadline = deadline.replace(hour=0, minute=0, second=0)

        created_on = datetime.now(timezone.utc)

        if not job_title or not salary or not deadline:
            return jsonify(message="Title, Salary and Deadline is mandatory fields"),400
        
        this_company = Company.query.filter_by(user_id=current_user.id).first()

        if not this_company:
            return jsonify(message="Company profile not found"),404

        if this_company.approval_status != "approved":
            return jsonify(message="This Company is not approved by Admin yet!"),403

        new_drive = PlacementDrive(
            company_id=this_company.id,
            job_title=job_title,
            job_description=job_description,
            salary=salary,
            eligibility_cgpa=eligibility_cgpa,
            eligibility_dept=eligibility_dept,
            deadline=deadline,
            created_on=created_on
        )

        db.session.add(new_drive)
        db.session.commit()
    return jsonify(message= "Placement drive created successfully"), 201


@company_bp.route('/update-status/<int:application_id>', methods=['POST'])
@jwt_required()
@role_required('company')
def updateStatus(application_id):

    if current_user.is_blacklisted:
        return jsonify(message="Blacklisted company cannot update status"), 403

    update_status = request.json.get("status")

    valid_status = ["applied","shortlisted","selected","rejected"]
    if update_status not in valid_status:
        return jsonify(message="Invalid status"),400

    application = Application.query.get_or_404(application_id)

    if application.drive.company.user_id != current_user.id:
        return jsonify(message="Unauthorized Action"), 403

    if application.status in ["selected","rejected"]:
        return jsonify(message=f"{application.status} application cannot be changed!"), 400

    if application.status == update_status:
        return jsonify(message="Status already set"),200

    application.status = update_status
    db.session.commit()

    return jsonify(
        message=f"Application status updated to {application.status}"
    ), 200


@company_bp.route("/close-drive/<int:drive_id>", methods=["POST"])
@jwt_required()
@role_required("company")
def closeDrive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)

    if current_user.is_blacklisted:
        return jsonify(message="Blacklisted company cannot close drives"), 403

    if drive.company.user_id != current_user.id:
        return jsonify(message="Unauthorized action"), 403

    if drive.status == "closed":
        return jsonify(message="Drive already closed"), 400

    drive.status = "closed"
    db.session.commit()

    return jsonify(message= "Drive closed successfully"), 200



@company_bp.route('/application/<int:application_id>', methods=['GET'])
@jwt_required()
def applicationDetails(application_id):

    application = Application.query.get_or_404(application_id)

    if current_user.is_blacklisted:
        return jsonify(message="Blacklisted company cannot view applications"), 403

    student = application.student
    drive = application.drive

    return jsonify({
        "student": {
            "id": student.id,
            "student_code": f"ST{student.id:03d}",
            "fullname": student.fullname,
            "department": student.department,
            "cgpa": student.cgpa,
            "year": student.year,
            "is_blacklisted": student.user.is_blacklisted
        },
        "drive": {
            "id": drive.id,
            "job_title": drive.job_title,
            "salary": float(drive.salary),
            "deadline": drive.deadline,
            "status": drive.status
        },
        "application": {
            "id": application.id,
            "status": application.status,
            "applied_on": application.application_date
        }
    }), 200



@company_bp.route('/view/applications/<int:drive_id>', methods=['GET'])
@jwt_required()
@role_required('company')
def viewApplications(drive_id):

    this_drive = PlacementDrive.query.get_or_404(drive_id)

    if current_user.is_blacklisted:
        return jsonify(message="Blacklisted company cannot view applications"), 403

    if this_drive.company.user_id != current_user.id:
        return jsonify(message="Unauthorized access"), 403

    applications = Application.query.outerjoin(Application.student).filter(Application.drive_id == drive_id).all()

    def serialize_application(application):
        student = application.student
        return {
            "application_id": application.id,
            "student_id": student.id,
            "student_name": student.fullname,
            "status": application.status,
            "applied_on": str(application.application_date)
            # "job_title": application.drive.job_title
        }

    result = [serialize_application(app) for app in applications]

    return jsonify({
        "applications": result,
        "job_title":this_drive.job_title
    }), 200


@company_bp.route("/drive/<int:drive_id>", methods=["GET"])
@jwt_required()
def getDriveDetails(drive_id):

    drive = PlacementDrive.query.get_or_404(drive_id)

    user_role = current_user.role

    already_applied = False

    if user_role == "student":
        application = Application.query.filter_by(
            student_id=current_user.id,
            drive_id=drive_id
        ).first()

        if application:
            already_applied = True

    return jsonify({
        "drive":{
            "id": drive.id,
            "job_title": drive.job_title,
            "job_description": drive.job_description,
            "company_name": drive.company.company_name,
            "salary": drive.salary,
            "eligibility_cgpa": drive.eligibility_cgpa,
            "eligibility_dept": drive.eligibility_dept,
            "deadline": drive.deadline.strftime("%Y-%m-%d")
        },
        "already_applied": already_applied
    }),200

@company_bp.route("/update-drive/<int:drive_id>", methods=["PUT"])
@jwt_required()
@role_required("company")
def updateDrive(drive_id):

    drive = PlacementDrive.query.get_or_404(drive_id)

    if current_user.is_blacklisted:
        return jsonify(message="Blacklisted company cannot update drives"),403

    if drive.company.user_id != current_user.id:
        return jsonify(message="Unauthorized access"),403

    if drive.status != "closed":
        return jsonify(message="Only closed drives can be edited"),400

    drive.job_title = request.json.get("job_title")
    drive.job_description = request.json.get("job_description")
    drive.salary = request.json.get("salary")
    drive.eligibility_cgpa = request.json.get("eligibility_cgpa")
    drive.eligibility_dept = request.json.get("eligibility_dept")
    drive.deadline = datetime.strptime(request.json.get("deadline"), "%Y-%m-%d")
    drive.status = 'active'
    drive.created_on = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify(message="Drive updated successfully"),200
