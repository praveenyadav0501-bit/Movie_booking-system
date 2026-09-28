from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_name = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    seats = Column(Integer, nullable=False)
    booked = Column(Boolean, default=False)