
-- Create tables
CREATE TABLE Users (
    User_ID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    Username VARCHAR(50),
    Password VARCHAR(50),
    Email VARCHAR(100),
    Phone_no VARCHAR(20),
    Address TEXT
);

CREATE TABLE Rooms (
    Room_no SERIAL PRIMARY KEY,
    Room_Type VARCHAR(50),
    Capacity INT,
    Description TEXT,
    Price_per_night DECIMAL(10, 2)
);

CREATE TABLE Bookings (
    Booking_ID SERIAL PRIMARY KEY,
    User_ID INT REFERENCES Users(User_ID),
    Room_no INT REFERENCES Rooms(Room_no),
    Check_in_Date DATE,
    Check_out_Date DATE,
    Total_Amount DECIMAL(10, 2)
);

CREATE TABLE Payments (
    Payment_ID SERIAL PRIMARY KEY,
    Booking_ID INT REFERENCES Bookings(Booking_ID),
    Payment_Date DATE,
    Amount DECIMAL(10, 2),
    Payment_Method VARCHAR(50)
);

CREATE TABLE Cancellations (
    Cancellation_ID SERIAL PRIMARY KEY,
    User_ID INT REFERENCES Users(User_ID),
    Booking_ID INT REFERENCES Bookings(Booking_ID),
    Reason TEXT
);

CREATE TABLE Reviews (
    Review_ID SERIAL PRIMARY KEY,
    Booking_ID INT REFERENCES Bookings(Booking_ID),
    Rating INT,
    Comment TEXT
);

CREATE TABLE Admins (
    Admin_ID SERIAL PRIMARY KEY,
    Username VARCHAR(50),
    Password VARCHAR(50),
    Name VARCHAR(100)
);
