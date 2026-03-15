from flask import Flask
from flask_cors import CORS
import os

from application.security import jwt
from application.config import LocalDevelopmentConfig

from application.database import db
from application.routes import auth_bp,admin_bp, company_bp, student_bp

from application.celery_init import celery_init_app
from celery.schedules import crontab

from application.seed_data import seed_demo_data

from application.cache_init import cache_init_app
from application.tasks import daily_deadline_reminder, monthly_activity_report

app = None

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    jwt.init_app(app)

    cache = cache_init_app(app)

    CORS(app)
    # CORS(app,supports_credentials=True)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(student_bp, url_prefix="/api/student")
    app.register_blueprint(company_bp, url_prefix="/api/company")

    app.app_context().push()
    return app

app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()

@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute = '*/2'),
        # crontab(hour=9, minute=0), # send email at 9 AM daily
        daily_deadline_reminder.s()
    )
    sender.add_periodic_task(
        crontab(minute = '*/2'), # Every 2 minitue
        # crontab(day_of_month=1, hour=9, minute=0), # Per month at 9AM
        monthly_activity_report.s()
    )

with app.app_context():   
    db.create_all()
    seed_demo_data()

    from application.models.user import User
    admin = User.query.filter_by(role="admin").first()

    if not admin:
        ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
        ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
        admin_user = User(username=ADMIN_USERNAME,fullname="Admin User",password=ADMIN_PASSWORD,role="admin")

        db.session.add(admin_user)
        db.session.commit()




@app.route("/")
def home():
    return "Flask Backend Running ✅"

if __name__ == "__main__":
    app.run()

