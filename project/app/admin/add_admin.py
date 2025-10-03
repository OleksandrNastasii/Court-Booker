import os
from flask import Blueprint
from werkzeug.security import generate_password_hash
from app.database.database import db_session
from app.models.user_model import UserModel

#Creates Blueprint for file to run at service boot
admin_user = Blueprint('admin_user', __name__)

#Creates /users webpage
@admin_user.route('/users', methods=['POST'])
def add_admin_user():
        
        #Try Except block for admin creation
        try: 

            #Retrieves admin credentials from env
            admin_name = os.getenv("ADMIN_USERNAME")
            admin_email = os.getenv("ADMIN_EMAIL")
            admin_password = os.getenv("ADMIN_PASSWORD")

            #Checks if admin user already exists
            admin = UserModel.query.filter_by(name=admin_name).first()
            if admin:
                print("Admin user already exists.")
                return
            
            #Creates admin user
            admin = UserModel(
                name=admin_name,
                email=admin_email,
                password=generate_password_hash(admin_password,  method='pbkdf2:sha256'),
                role="admin"
            )

            #Adds and commits admin to the database
            db_session.add(admin)
            db_session.commit()
            print("Admin user created successfully.")

        except:
             pass

#Starts add_admin_user() if file was run directly
if __name__ == "__main__":
    add_admin_user()
