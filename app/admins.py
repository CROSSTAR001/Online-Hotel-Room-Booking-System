import streamlit as st
import pandas as pd
from database import session, Booking, User, Room, Payment, Cancellation, Review
from datetime import date

def admin_dashboard(admin):
    st.subheader("Admin Dashboard")
    st.text(f"Welcome {admin.name}")

    task = st.selectbox("Task", ["View Customers", "Manage Bookings", "View Room Status"])

    if task == "View Customers":
        st.subheader("Customers List")
        customers = session.query(User).all()
        if customers:
            for customer in customers:
                st.text(f"Name: {customer.name}, Username: {customer.username}, Email: {customer.email}, Phone: {customer.phone_no}")
        else:
            st.text("No customers found")

    elif task == "Manage Bookings":
        st.subheader("Manage Bookings")
        bookings = session.query(Booking, User).join(User, Booking.user_id == User.user_id).all()
        if bookings:
            for booking, user in bookings:
                payment = session.query(Payment).filter(Payment.booking_id == booking.booking_id).first()
                cancellation = session.query(Cancellation).filter(Cancellation.booking_id == booking.booking_id).first()
                review = session.query(Review).filter(Review.booking_id == booking.booking_id).first()
                
                st.text(f"Booking ID: {booking.booking_id}, Room No: {booking.room_no}, Customer: {user.name}, Check-in: {booking.check_in_date}, Check-out: {booking.check_out_date}")
                st.text(f"Total Amount: {booking.total_amount}, Payment: {'Yes' if payment else 'No'}, Cancelled: {'Yes' if cancellation else 'No'}, Reviewed: {'Yes' if review else 'No'}")

                if not payment:
                    st.text("Accept Payment:")
                    with st.form(key=f"payment_form_{booking.booking_id}"):
                        payment_method = st.selectbox("Payment Method", ["UPI", "Netbanking", "Credit Card", "Debit Card"])
                        submit_payment = st.form_submit_button("Confirm Payment")
                        if submit_payment:
                            new_payment = Payment(
                                booking_id=booking.booking_id,
                                payment_date=date.today(),
                                amount=booking.total_amount,
                                payment_method=payment_method
                            )
                            session.add(new_payment)
                            session.commit()
                            st.experimental_rerun()
                st.text("---")
        else:
            st.text("No bookings found")

    elif task == "View Room Status":
        st.subheader("Room Status")
        rooms = session.query(Room).all()
        room_data = []
        for room in rooms:
            bookings = session.query(Booking).filter(Booking.room_no == room.room_no).all()
            for booking in bookings:
                user = session.query(User).filter(User.user_id == booking.user_id).first()
                payment = session.query(Payment).filter(Payment.booking_id == booking.booking_id).first()
                cancellation = session.query(Cancellation).filter(Cancellation.booking_id == booking.booking_id).first()
                review = session.query(Review).filter(Review.booking_id == booking.booking_id).first()

                room_data.append([
                    room.room_no,
                    user.name if user else "Unknown",
                    booking.check_in_date,
                    booking.check_out_date,
                    f"{booking.total_amount}",
                    "Yes" if payment else "No",
                    "Yes" if cancellation else "No",
                    "Yes" if review else "No"
                ])

        if room_data:
            df = pd.DataFrame(room_data, columns=["Room No", "Customer Name", "Check-in Date", "Check-out Date", "Total Amount", "Payment", "Cancelled", "Reviewed"])
            st.dataframe(df)
        else:
            st.text("No room status data found")
