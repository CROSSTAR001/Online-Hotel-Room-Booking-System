# Hotel Room Booking System

This is a Hotel Room Booking System built using Streamlit, SQLAlchemy, and PostgreSQL. The application allows users to book hotel rooms, view their booking history, leave reviews, and manage their bookings. Admins can view customers, manage bookings, accept payments, and get a tabular view of room statuses.

## Features

- User authentication (sign up and log in)
- Room booking with payment integration
- View booking history and leave reviews
- Admin dashboard to manage bookings and payments
- Background image with reduced opacity
- Custom favicon and tab name

## Database Configuration

- Create a database names 'hotel_management'
- run the TABLE.sql file using PgAdmin
- App/config.py includes the database name, userid and password (or you can edit it out for your own)

## Installation

1. Clone the repository:

      git clone https://github.com/CROSSTAR001/hotel-booking-system.git  <br>
      cd hotel-booking-system

2. Install the required packages:

      pip install -r requirements.txt

3. Run the Streamlit application:

      streamlit run app.py
