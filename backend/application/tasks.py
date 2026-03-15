from celery import shared_task
import csv
from jinja2 import Template
import datetime
from .mail import send_email

from application.models.user import User
from application.models.company import Company
from application.models.placementDrive import PlacementDrive
from application.models.application import Application


# task1 : Scheduled Job - Daily reminders 
    # - Send reminders to students about upcoming application deadlines via email, SMS, or chat webhook, daily at a chosen time

@shared_task(ignore_result=False, name="daily_deadline_reminder")
def daily_deadline_reminder():

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    # find drives whose deadline is tomorrow
    # upcoming_drives = PlacementDrive.query.filter(PlacementDrive.deadline == tomorrow).all()
    # upcoming_drives = PlacementDrive.query.filter(PlacementDrive.deadline >= today).all()
    upcoming_drives = PlacementDrive.query.filter(PlacementDrive.status=='active').all()
    students = User.query.filter_by(role="student").all()

    for student in students:
        pending_drives = []
        for drive in upcoming_drives:

            # check if student already applied
            application = Application.query.filter_by( student_id=student.id, drive_id=drive.id ).first()
            
            if not application:
                drive_info = {}
                drive_info["company"] = drive.company.company_name
                drive_info["title"] = drive.job_title
                drive_info["deadline"] = drive.deadline
                pending_drives.append(drive_info)

        # skip if student already applied to all
        if len(pending_drives) == 0:
            continue
        user_data = {
            "username": student.username,
            "drives": pending_drives
        }
# Mail template start
        mail_template = """
        <h3>Dear {{user_data.username}}</h3>

        <p>This is a reminder about placement drives whose application deadline is tomorrow.</p>

        <table border="1">
            <tr>
                <th>Company</th>
                <th>Drive Title</th>
                <th>Deadline</th>
            </tr>

            {% for drive in user_data.drives %}
            <tr>
                <td>{{drive.company}}</td>
                <td>{{drive.title}}</td>
                <td>{{drive.deadline}}</td>
            </tr>
            {% endfor %}

        </table>

        <p>Please apply before the deadline.</p>

        <p>Visit the placement portal for details.</p>

        <h5>Regards</h5>
        <h5>PlaceMint</h5>
        """
# Mail template end
        message = Template(mail_template).render(user_data=user_data)

        send_email(
            student.username,
            subject="Placement Drive Deadline Reminder",
            message=message
        )

    return "Daily reminder emails sent"



# task2 : Scheduled Job - Monthly Activity Report For Admin
    # -- Number of drives conducted , Number of students applied and selected
    # Report generated on the first day of every month.
    # Sent to admin via email.

@shared_task(ignore_result=False, name="monthly_activity_report")
def monthly_activity_report():

    admin = User.query.filter_by(role="admin").first()

    # calculate last month period
    today = datetime.date.today()
    first_day_this_month = today.replace(day=1)
    last_month_end = first_day_this_month - datetime.timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    drives = PlacementDrive.query.filter( PlacementDrive.created_on >= last_month_start, PlacementDrive.created_on <= last_month_end ).all()

    number_of_drives = len(drives)


    applications = Application.query.filter( Application.application_date >= last_month_start, Application.application_date <= last_month_end ).all()

    students_applied = len(applications)

    selected_students = len([a for a in applications if a.status == "Selected"])

    report_data = {
        "month": last_month_start.strftime("%B %Y"),
        "drives": number_of_drives,
        "applied": students_applied,
        "selected": selected_students
    }

# HTML mail template
    mail_template = """
    <h2>Monthly Placement Activity Report</h2>

    <p>Dear Admin,</p>

    <p>Please find the placement report for <b>{{report.month}}</b>.</p>

    <table border="1" cellpadding="6">
        <tr>
            <th>Metric</th>
            <th>Count</th>
        </tr>

        <tr>
            <td>Number of Drives Conducted</td>
            <td>{{report.drives}}</td>
        </tr>

        <tr>
            <td>Students Applied</td>
            <td>{{report.applied}}</td>
        </tr>

        <tr>
            <td>Students Selected</td>
            <td>{{report.selected}}</td>
        </tr>

    </table>

    <br>

    <p>Regards,<br>
    PlaceMint</p>
    """
# html page end
    message = Template(mail_template).render(report=report_data)

    # send email
    send_email(
        admin.username,
        subject="Monthly Placement Activity Report",
        message=message
    )

    return "Monthly activity report sent to admin"




# task3 : User Triggered Async Job – Export Applications as CSV
#         Students can export their placement application history.
#         CSV should include:
    #         Student ID
    #         Company Name
    #         Drive Title
    #         Application Status
    #         Dates
#         Export is triggered from the student dashboard.
#         This should trigger a batch job, and send an alert once done.

@shared_task(ignore_result=False, name="export_application_history_csv_report")
def export_application_history(student_id):

  
    applications = Application.query.filter_by(student_id=student_id).all()
    print("Applications found:", len(applications))
    # create unique file name
    csv_file_name = f"applications_{student_id}_{datetime.datetime.now().strftime('%f')}.csv"

    with open(f"static/{csv_file_name}", "w", newline="") as csvfile:
        sr_no = 1
        csv_writer = csv.writer(csvfile, delimiter=",")

        # header
        csv_writer.writerow([ "Sr No.", "Application ID", "Company Name", "Drive Title","Offered Salary","Application Status", "Application Date"])

        # rows
        for app in applications:
            row = [ sr_no, app.id, app.drive.company.company_name, app.drive.job_title, app.drive.salary, app.status, app.application_date]

            csv_writer.writerow(row)
            sr_no += 1

    # return file name 
    return csv_file_name