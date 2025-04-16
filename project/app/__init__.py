from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv

from .database.database import init_db
from .config.config import Secret_Key

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Secret_Key)

    from .models.user_model import UserModel

    init_db()

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    from app.auth.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.routes.user_routes import user_routes as user_routes_blueprint
    app.register_blueprint(user_routes_blueprint)

    return app
