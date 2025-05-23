from flask_login import UserMixin

from ..database.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class UserModel(UserMixin, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(254), unique=True)
    password = Column(String(255))
    role = Column(String(255), default="user")

    bookings = relationship("BookingModel", back_populates="user")

    def is_admin(self):
        return self.role == "admin"
    
    def is_moderator(self):
        return self.role == "moderator"
    
    def show_user(self):
        return ({
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role
            })

class BookingModel(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    court_id = Column(Integer, ForeignKey('courts.id'), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    token = Column(String(255), unique=True)
    status = Column(Boolean, default=True)

    user = relationship("UserModel", back_populates="bookings")
    court = relationship("CourtModel", back_populates="bookings")

    def show_booking(self):
        return ({
            "id": self.id,
            "user_id": self.user_id,
            "court_id": self.court_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "token": self.token,
            "status": self.status
            })

class CourtModel(Base):
    __tablename__ = "courts"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    location = Column(String(255), nullable=True)

    bookings = relationship("BookingModel", back_populates="court")

    def show_court(self):
        return ({
            "id": self.id,
            "name": self.name,
            "location": self.location,
            })