from app import app,datastore
from backend.models.model import db,User,Role
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name='admin',description="user is admin")
    datastore.find_or_create_role(name='user',description="user is user")
    db.session.commit()

    if not datastore.find_user(email= "admin@gmail.com"):
        datastore.create_user(email="admin@gmail.com",first_name="admin",username ="admin",password = generate_password_hash("admin"),roles=["admin"])

    if not datastore.find_user(email="user@gmail.com"):
        datastore.create_user(email="user@gmail.com",first_name="user",username="user",password=generate_password_hash("user"),roles=["user"])
    db.session.commit()