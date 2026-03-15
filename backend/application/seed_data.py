from datetime import datetime, timedelta

from application.database import db
from application.models.user import User
from application.models.student import Student
from application.models.company import Company
from application.models.placementDrive import PlacementDrive
from application.models.application import Application


def seed_demo_data():
    
    if User.query.first():
        return

    student_users = [
        User(username="rahul@gmail.com", fullname="Rahul Sharma", password="1234", role="student"),
        User(username="ananya@gmail.com", fullname="Ananya Das", password="1234", role="student"),
        User(username="rohit@gmail.com", fullname="Rohit Sen", password="1234", role="student"),
    ]

    db.session.add_all(student_users)
    db.session.commit()

    students = [
        Student(user_id=student_users[0].id, fullname="Rahul Sharma", department="CSE", cgpa=8.5, year=4),
        Student(user_id=student_users[1].id, fullname="Ananya Das", department="CSE", cgpa=9.1, year=4),
        Student(user_id=student_users[2].id, fullname="Rohit Sen", department="IT", cgpa=7.8, year=4),
    ]

    db.session.add_all(students)
    db.session.commit()



    company_users = [
        User(username="hr@tcs.com", fullname="TCS HR", password="1234", role="company"),
        User(username="hr@infosys.com", fullname="Infosys HR", password="1234", role="company"),
    ]

    db.session.add_all(company_users)
    db.session.commit()

    companies = [
        Company(
            user_id=company_users[0].id,
            company_name="TCS",
            hr_contact="9876543210",
            website="https://tcs.com",
            location="Bangalore",
            approval_status="approved"
        ),
        Company(
            user_id=company_users[1].id,
            company_name="Infosys",
            hr_contact="9876501234",
            website="https://infosys.com",
            location="Hyderabad",
            approval_status="approved"
        )
    ]

    db.session.add_all(companies)
    db.session.commit()



    companies = Company.query.all()

    drives = [
        PlacementDrive(
            company_id=companies[0].id,
            job_title="Software Engineer",
            job_description="Backend developer role",
            salary=8.5,
            eligibility_cgpa=7.0,
            eligibility_dept="CSE,IT",
            deadline=datetime.utcnow() + timedelta(days=10),
            status="active",
            created_on=datetime.utcnow()
        ),
        PlacementDrive(
            company_id=companies[1].id,
            job_title="Data Analyst",
            job_description="Business data analysis",
            salary=7.0,
            eligibility_cgpa=6.5,
            eligibility_dept="CSE,IT,ECE",
            deadline=datetime.utcnow() + timedelta(days=15),
            status="active",
            created_on=datetime.utcnow()
        )
    ]

    db.session.add_all(drives)
    db.session.commit()


    students = Student.query.all()
    drives = PlacementDrive.query.all()


    applications = [
        Application(
            student_id=students[0].id,
            drive_id=drives[0].id,
            application_date=datetime.utcnow(),
            status="applied"
        ),
        Application(
            student_id=students[1].id,
            drive_id=drives[0].id,
            application_date=datetime.utcnow(),
            status="shortlisted"
        ),
        Application(
            student_id=students[2].id,
            drive_id=drives[1].id,
            application_date=datetime.utcnow(),
            status="selected"
        ),
    ]

    db.session.add_all(applications)
    db.session.commit()