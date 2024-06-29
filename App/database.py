from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config

# Database setup
engine = create_engine(config.DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define tables based on the schema
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    username = Column(String(50))
    password = Column(String(50))
    email = Column(String(100))
    phone_no = Column(String(20))
    address = Column(Text)

class Room(Base):
    __tablename__ = 'rooms'
    room_no = Column(Integer, primary_key=True)
    room_type = Column(String(50))
    capacity = Column(Integer)
    description = Column(Text)
    price_per_night = Column(DECIMAL(10, 2))

class Booking(Base):
    __tablename__ = 'bookings'
    booking_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    room_no = Column(Integer, ForeignKey('rooms.room_no'))
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    total_amount = Column(DECIMAL(10, 2))

class Payment(Base):
    __tablename__ = 'payments'
    payment_id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'))
    payment_date = Column(Date)
    amount = Column(DECIMAL(10, 2))
    payment_method = Column(String(50))

class Cancellation(Base):
    __tablename__ = 'cancellations'
    cancellation_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'))
    reason = Column(Text)

class Review(Base):
    __tablename__ = 'reviews'
    review_id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'))
    rating = Column(Integer)
    comment = Column(Text)

class Admin(Base):
    __tablename__ = 'admins'
    admin_id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(50))
    name = Column(String(100))

Base.metadata.create_all(engine)