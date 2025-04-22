# from ..database.database import Base
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship


# class CourtModel(Base):
#     __tablename__ = "courts"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255))
#     location = Column(String(255))

#     bookings = relationship("BookingModel", back_populates="court")
