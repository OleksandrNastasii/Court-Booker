# from ..database.database import Base
# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy.orm import relationship

# class BookingModel(Base):
#     __tablename__ = "booking"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     court_id = Column(Integer, ForeignKey('courts.id'), nullable=False)
#     start_time = Column(DateTime, nullable=False)
#     end_time = Column(DateTime, nullable=False)
#     token = Column(String(255), unique=True)
#     status = Column(String(255), default='active')

#     user = relationship("UserModel", back_populates="bookings")
#     court = relationship("CourtModel", back_populates="bookings")