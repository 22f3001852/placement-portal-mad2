from flask import Blueprint, request, jsonify,abort, redirect, url_for, Response
from application.database import db
from application.models.user import User
from application.models.student import Student
from application.models.company import Company
from application.models.placementDrive import PlacementDrive
from application.models.application import Application
from flask_jwt_extended import create_access_token,current_user,jwt_required
from application.utils.decorator import role_required
from datetime import datetime,timezone
from application.cache_init import cache
# import pytz

# IST = pytz.timezone('Asia/Kolkata')

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=["POST"])
def login():

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none()
    if not user or user.password != password:
        return jsonify("Enter Correct Username or Password!"), 400

    if user.is_blacklisted == True:
        return jsonify(message= "You are blacklisted by the admin!"),403
    
    access_token = create_access_token(identity=user)
    role = user.role
    return jsonify(access_token=access_token, role=role)


@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", None)
    fullname = request.form.get("fullname", None)
    department = request.form.get("department", None)
    password = request.form.get("password", None)
    role = request.form.get("role", None)

    if not username or not password or not role:
        return jsonify(message="Missing required fields"), 400 #400 for bad request

    this_user = User.query.filter_by(username=username).one_or_none()
    if this_user:
        return jsonify(message="Username already exists"), 409 #409 for conflict
    
    new_user = User(username=username, fullname=fullname, password=password, role=role)
    db.session.add(new_user)
    db.session.flush() # to get the new user's ID for the foreign key relationship in Student and Company tables

    if role == "student":
        cgpa = request.form.get("cgpa", None)
        year = request.form.get("year", None)

        if 'resume' in request.files:
            resume = request.files['resume']
            if resume.filename == '':
                resume_bytes = None
            elif resume:
                resume_bytes = resume.read()
            else:
                return jsonify({"message": "Invalid file type. Only PDF allowed."}), 400
        else:
            resume_bytes = None

        new_student = Student(user=new_user, fullname=fullname, department=department, cgpa=cgpa, year=year, resume=resume_bytes)
        db.session.add(new_student)

    elif role == "company":
        company_name = request.form.get("companyName", None)
        hr_contact = request.form.get("hrContact", None)
        website = request.form.get("website", None)
        location = request.form.get("location", None)

        new_company = Company(user=new_user, company_name=company_name, hr_contact=hr_contact, website=website, location=location)
        db.session.add(new_company)
    else:
        return jsonify(message="Invalid role"), 400
    
    db.session.commit()

    return jsonify(message="User registered successfully"), 201 #201 for successful resource creation


@auth_bp.route("/dashboard",methods=['GET'])
@jwt_required()
def dashboard():
    if current_user.role == "admin":

        # auto close expired drives
        expired_drives = PlacementDrive.query.filter(PlacementDrive.status == "active",PlacementDrive.deadline < datetime.now(timezone.utc)).all()

        for drive in expired_drives:
            drive.status = "closed"

        db.session.commit()

        no_of_students = db.session.query()
        no_of_students = Student.query.join(Student.user).filter(User.is_blacklisted == False).count()
        no_of_companies = Company.query.join(Company.user).filter(Company.approval_status == "approved",User.is_blacklisted == False).count()

        no_of_active_drives = PlacementDrive.query.filter_by(status="active").count()

        no_of_approved_companies = Company.query.filter_by(approval_status="approved").count()
        no_of_pending_comapanies = Company.query.filter_by(approval_status="pending").count()

        no_of_placed_students = Application.query.filter_by(status="selected").count()

        total_package = db.session.query(db.func.sum(PlacementDrive.salary))\
            .join(Application)\
            .filter(Application.status == "selected")\
            .scalar() or 0

        average_package = total_package / no_of_placed_students if no_of_placed_students > 0 else 0

        applications = Application.query.all()

        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

        applied_data = [0]*7
        shortlisted_data = [0]*7

        for each_application in applications:
            if not each_application.application_date:
                continue

            weekday = each_application.application_date.weekday()

            if each_application.status == "applied":
                applied_data[weekday] += 1
            elif each_application.status == "shortlisted":
                shortlisted_data[weekday] += 1

        return jsonify({
            "role": current_user.role,
            "stats":{
                "students": no_of_students,
                "companies": no_of_companies,
                "active_drives": no_of_active_drives,
                "average_package": average_package
            },
            "charts":{
                "labels": days,
                "applied_data": applied_data,
                "shortlisted_data": shortlisted_data,
                "approved_company": no_of_approved_companies,
                "pending_company": no_of_pending_comapanies
            }
        })
    elif current_user.role == "company":
        if current_user.is_blacklisted:
            return jsonify(message= "Blacklisted company cannot access dashboard!"),403
        

        company = Company.query.filter_by(user_id=current_user.id).first()

        if not company:
            return jsonify(message="Company profile not found"), 404

        expired_drives = PlacementDrive.query.filter(PlacementDrive.company_id == company.id,PlacementDrive.status == "active",PlacementDrive.deadline <datetime.now(timezone.utc)).all()

        for drive in expired_drives:
            drive.status = "closed"

        db.session.commit()

        ongoing_drives = PlacementDrive.query.filter_by(company_id=company.id,status="active").all()
        closed_drives = PlacementDrive.query.filter_by(company_id=company.id,status="closed").all()

        # Serialize drives (we need serialization bcoz sqlalchemy objects are not json friendly)
        def serialize_drive(drive):
            created_on = drive.created_on.replace(tzinfo=timezone.utc)
            return {
                "id": drive.id,
                "drive_code": f"DRV{drive.id:03d}",
                "job_title": drive.job_title,
                "salary": float(drive.salary) if drive.salary else None,
                "deadline": str(drive.deadline),
                "status": drive.status,
                "created_on": created_on
            }

        return jsonify({
            "company": {
                "id": company.id,
                "name": company.company_name
            },
            "drives": {
                "ongoing": [serialize_drive(drive) for drive in ongoing_drives],
                "closed": [serialize_drive(drive) for drive in closed_drives]
            }
        }), 200
    elif current_user.role == "student":
        student = Student.query.filter_by(user_id=current_user.id).first()

    # approved companies
        companies = Company.query.join(Company.user).filter(Company.approval_status == "approved",User.is_blacklisted == False).all()

        organizations = [
            {
                "id":each_company.id,
                "name":each_company.company_name
            }
            for each_company in companies
        ]

        # applied drives
        applications = Application.query.filter_by(student_id=student.id).all()
        applied_drives = []
        for each_application in applications:
            drive = PlacementDrive.query.get(each_application.drive_id)
            applied_drives.append({
                "id":drive.id,
                "job_title":drive.job_title,
                "company_name":drive.company.company_name,
                "applied_on":each_application.application_date,
                "status":each_application.status
            })
        
        return jsonify({
            "organizations":organizations,
            "applied_drives":applied_drives
        })



@auth_bp.route("/profile", methods=["GET","PUT"])
@jwt_required()
def profile():

    user_id = current_user.id
    user = User.query.get(user_id)

    if request.method == "GET":

        if user.role == "student":
            student = Student.query.filter_by(user_id=user_id).first()

            return jsonify({
                "user_id":user.id,
                "username":user.username,
                "name": student.fullname,
                "department": student.department,
                "cgpa": student.cgpa,
                "year":student.year,
                "has_resume": True if student.resume else False

            })

        if user.role == "company":
            company = Company.query.filter_by(user_id=user_id).first()

            return jsonify({
                "user_id":user.id,
                "username":user.username,
                "fullname":user.fullname,
                "company_name": company.company_name,
                "hr_contact": company.hr_contact,
                "website": company.website,
                "location": company.location,
                "approval_status": company.approval_status
            })

    if request.method == "PUT":
        if user.is_blacklisted:
            return jsonify(message= "Blacklisted User can not Update details!"),403
        
        if user.role == "student":
            student = Student.query.filter_by(user_id=user_id).first()

            student.fullname = request.form.get("name") 
            student.department = request.form.get("department")
            student.cgpa = request.form.get("cgpa")
            student.year = request.form.get("year")

            if 'resume' in request.files and request.files['resume'].filename != '':
                resume = request.files['resume']
                
                if not resume.filename.endswith(".pdf"):
                    return jsonify({"message": "Only PDF files allowed"}), 400

                student.resume = resume.read()

        if user.role == "company":
            company = Company.query.filter_by(user_id=user_id).first()

            company.user.fullname = request.form.get("fullname")
            company.company_name = request.form.get("company_name")
            company.hr_contact = request.form.get("hr_contact")
            company.website = request.form.get("website")
            company.location = request.form.get("location")
            

        db.session.commit()

        return jsonify({"message":"Profile updated"})

@auth_bp.route("/resume/<int:user_id>", methods=["GET"])
def get_resume(user_id):

    # user_id = current_user.id
    student = Student.query.filter_by(user_id=user_id).first()

    if not student.resume:
        return jsonify({"message": "No resume uploaded"}), 404

    return Response(
        student.resume,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": "inline; filename=resume.pdf"
        }
    )








