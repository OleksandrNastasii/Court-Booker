from threading import Thread
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv

from .database.database import init_db
from .config.config import Secret_Key
from app.routes.booking.booking import booking as booking_blueprint


load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Secret_Key)

    from app.models.user_model import UserModel, BookingModel, CourtModel
    # from .models.booking_model import BookingModel
    # from .models.playing_court_model import CourtModel

    init_db()

    login_manager = LoginManager()
    login_manager.init_app(app)
    # login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(int(user_id))

    from app.auth.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.routes.user_routes import user_routes as user_routes_blueprint
    app.register_blueprint(user_routes_blueprint)

    from app.routes.users import user as users_blueprint
    app.register_blueprint(users_blueprint)

    app.register_blueprint(booking_blueprint)

    from app.routes.booking.book import book
    app.register_blueprint(book)

    from app.routes.booking.verify import verify as verify_blueprint
    app.register_blueprint(verify_blueprint)

    from app.routes.courts.courts import courts_bp
    app.register_blueprint(courts_bp)

    from app.routes.courts.list import courts_list_bp
    app.register_blueprint(courts_list_bp)

    from app.routes.dashboards import dashboard
    app.register_blueprint(dashboard)

    return app
