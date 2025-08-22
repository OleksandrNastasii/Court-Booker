import os
from flask import Blueprint
from werkzeug.security import generate_password_hash
from app.database.database import db_session
from app.models.user_model import UserModel

admin_user = Blueprint('admin_user', __name__)

@admin_user.route('/users', methods=['POST'])
def add_admin_user():
        try: 
            admin_name = os.getenv("ADMIN_USERNAME", "admin")
            admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
            admin_password = os.getenv("ADMIN_PASSWORD", "admin123123")

            # Check if admin user already exists
            admin = UserModel.query.filter_by(name=admin_name).first()
            if admin:
                print("Admin user already exists.")
                return
            
            # Create admin user
            admin = UserModel(
                name=admin_name,
                email=admin_email,
                password=generate_password_hash(admin_password,  method='pbkdf2:sha256'),
                role="admin"
            )
            db_session.add(admin)
            db_session.commit()
            print("Admin user created successfully.")

        except:
             pass

if __name__ == "__main__":
    add_admin_user()
