from flask_login import UserMixin

from ..database.database import Base
from sqlalchemy import Column, Integer, String

class UserModel(UserMixin, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(254), unique=True)
    password = Column(String(255))