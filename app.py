from flask import Flask
from flask_security import Security
from flask_cors import CORS
from flask_security import SQLAlchemyUserDatastore
from flask_migrate import Migrate
from backend.models.model import db,User,Role
from config import DevelopmentConfig
from backend.resource.resource import api
import flask_excel as excel
from backend.tasks.worker import celery_init_app
from celery.schedules import crontab
from backend.tasks.tasks import daily_reminder
from datetime import datetime,timedelta
#from application.payment import payment_bp

migrate = Migrate()

datastore = SQLAlchemyUserDatastore(db, User, Role)

def create_app(): #defining app instance function
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    CORS(app)
    db.init_app(app) #initializing the database
    migrate.init_app(app,db)
    api.init_app(app) #initializing the api instance
    excel.init_excel(app)
    app.security = Security(app,datastore)
    
    # #app.register_blueprint(payment_bp, url_prefix='/api/payment')

    
        # import application.views

    return app

app = create_app() #calling function to create app
celery_app = celery_init_app(app)

#this is not triggered intead it is auto start/triggered

@celery_app.on_after_configure.connect
def periodic_task(sender,**kwargs):
    sender.add_periodic_task(1.0,daily_reminder.s("This is a reminder that you have not logged in for over 24 hours. Please log in to your account to continue using our services."),name='add every 10 s')
    sender.add_periodic_task(
          crontab(hour=13,minute=5,day_of_week=2),
          daily_reminder.s('Please visit the app')
      )

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
