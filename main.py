from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import Base, engine, LocalSession
from models import Booking

app = FastAPI(title="Movie Booking System API")

Base.metadata.create_all(bind=engine)


# Request model
class BookingRequest(BaseModel):
    movie_name: str = Field(min_length=1, max_length=100)
    customer_name: str = Field(min_length=1, max_length=100)
    seats: int = Field(gt=0)
    booked: bool = False


# Update model
class BookingUpdate(BaseModel):
    movie_name: str | None = None
    customer_name: str | None = None
    seats: int | None = None
    booked: bool | None = None


@app.get("/")
def home():
    return {"message": "Welcome to Movie Booking System API"}


# Create Booking
@app.post("/bookings")
def create_booking(request: BookingRequest):
    db = LocalSession()

    booking = Booking(
        movie_name=request.movie_name,
        customer_name=request.customer_name,
        seats=request.seats,
        booked=request.booked
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    db.close()

    return {
        "message": "Booking created successfully",
        "data": booking
    }


# Get All Bookings
@app.get("/bookings")
def get_bookings():
    db = LocalSession()

    bookings = db.query(Booking).all()

    db.close()

    return bookings


# Get Booking By ID
@app.get("/bookings/{booking_id}")
def get_booking(booking_id: int):
    db = LocalSession()

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    db.close()

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return booking


# Update Booking
@app.put("/bookings/{booking_id}")
def update_booking(
    booking_id: int,
    request: BookingUpdate
):
    db = LocalSession()

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if booking is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if request.movie_name is not None:
        booking.movie_name = request.movie_name

    if request.customer_name is not None:
        booking.customer_name = request.customer_name

    if request.seats is not None:
        booking.seats = request.seats

    if request.booked is not None:
        booking.booked = request.booked

    db.commit()
    db.refresh(booking)
    db.close()

    return {
        "message": "Booking updated successfully",
        "data": booking
    }


# Delete Booking
@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int):
    db = LocalSession()

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if booking is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    db.delete(booking)
    db.commit()
    db.close()

    return {
        "message": "Booking deleted successfully"
    }