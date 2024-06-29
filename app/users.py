import streamlit as st
from database import session, Room, Booking, Payment, Review, Cancellation, User
from datetime import date, timedelta
import time

def user_dashboard(user):
    st.subheader("User Dashboard")
    st.text(f"Welcome {user.name}")

    task = st.selectbox("Task", ["View Available Rooms", "View Booking History", "Leave a Review"])

    # Clear the selected room and cancel booking if task changes
    if st.session_state.get("current_task") != task:
        st.session_state.selected_room = None
        st.session_state.cancelling_booking = None
        st.session_state.viewing_reviews = None
        st.session_state.task = None
        st.session_state.current_task = task

    if task == "View Available Rooms":
        st.subheader("Available Rooms")
        rooms = session.query(Room).all()
        for room in rooms:
            col1, col2 = st.columns([5, 2])
            with col1:
                if st.button(f"Room No: {room.room_no}, Type: {room.room_type}, Capacity: {room.capacity}, Price: {room.price_per_night}"):
                    st.session_state.selected_room = room
                    st.session_state.task = "Make a Booking"
                    st.experimental_rerun()
            with col2:
                if st.button(f"View Reviews", key=f"reviews_{room.room_no}"):
                    st.session_state.viewing_reviews = room.room_no
                    st.experimental_rerun()

    if st.session_state.get("task") == "Make a Booking" and "payment_done" not in st.session_state:
        st.subheader("Make a Booking")
        selected_room = st.session_state.get("selected_room")

        if not selected_room:
            rooms = session.query(Room).all()
            room_options = {f"Room No: {room.room_no}, Type: {room.room_type}": room for room in rooms}
            room_choice = st.selectbox("Select Room", list(room_options.keys()))
            selected_room = room_options[room_choice]
        
        check_in_date = st.date_input("Check-in Date", value=date.today(), min_value=date.today())
        check_out_date = st.date_input("Check-out Date", value=date.today() + timedelta(days=1), min_value=date.today() + timedelta(days=1))
        
        if check_in_date and check_out_date:
            num_nights = (check_out_date - check_in_date).days
            total_amount = num_nights * selected_room.price_per_night
            st.text(f"Total Amount: ${total_amount:.2f}")

        if st.button("Proceed to Payment"):
            st.session_state.booking_info = {
                "user_id": user.user_id,
                "room_no": selected_room.room_no,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "total_amount": total_amount
            }
            st.session_state.payment_stage = "payment"
            st.experimental_rerun()

    elif task == "View Booking History":
        st.subheader("Booking History")
        bookings = session.query(Booking).filter(Booking.user_id == user.user_id).all()
        if bookings:
            for booking in bookings:
                st.text(f"Booking ID: {booking.booking_id}, Room No: {booking.room_no}, Check-in: {booking.check_in_date}, Check-out: {booking.check_out_date}, Amount: {booking.total_amount}")
                
                cancellation = session.query(Cancellation).filter(Cancellation.booking_id == booking.booking_id).first()
                if cancellation:
                    st.text(f"Cancelled: {cancellation.reason}")
                else:
                    if st.button("Cancel Booking", key=f"cancel_{booking.booking_id}"):
                        st.session_state.cancelling_booking = booking.booking_id
                        st.experimental_rerun()
                
                st.text("---")
        else:
            st.text("No bookings done")

    if st.session_state.get("cancelling_booking"):
        st.subheader("Cancel Booking")
        booking_id = st.session_state.cancelling_booking
        reason = st.text_area("Reason for Cancellation")
        if st.button("Submit Cancellation"):
            booking = session.query(Booking).filter(Booking.booking_id == booking_id).first()
            new_cancellation = Cancellation(
                user_id=booking.user_id,
                booking_id=booking.booking_id,
                reason=reason
            )
            session.add(new_cancellation)
            session.commit()
            session.delete(booking)
            session.commit()
            st.success("Booking cancelled successfully.")
            del st.session_state.cancelling_booking
            st.experimental_rerun()

    elif task == "Leave a Review":
        st.subheader("Leave a Review")
        bookings = session.query(Booking).filter(Booking.user_id == user.user_id).all()
        if bookings:
            booking_options = {f"Booking ID: {booking.booking_id}": booking for booking in bookings}
            booking_choice = st.selectbox("Select Booking", list(booking_options.keys()))
            
            if booking_choice:
                selected_booking = booking_options[booking_choice]

                rating = st.slider("Rating", 1, 5)
                comment = st.text_area("Comment")

                if st.button("Submit Review"):
                    new_review = Review(
                        booking_id=selected_booking.booking_id,
                        rating=rating,
                        comment=comment
                    )
                    session.add(new_review)
                    session.commit()
                    st.success("Review submitted!")
        else:
            st.text("No bookings done to review")

    if st.session_state.get("viewing_reviews"):
        st.subheader("Room Reviews")
        room_no = st.session_state.viewing_reviews
        reviews = session.query(Review, User).join(Booking, Review.booking_id == Booking.booking_id).join(User, Booking.user_id == User.user_id).filter(Booking.room_no == room_no).all()
        if reviews:
            for review, reviewer in reviews:
                st.text(f"Reviewer: {reviewer.name}")
                st.text(f"Rating: {'★' * review.rating}{'☆' * (5 - review.rating)}")
                st.text(f"Comment: {review.comment}")
                st.text("---")
        else:
            st.text("No reviews for this room")
        if st.button("Back to Available Rooms"):
            del st.session_state.viewing_reviews
            st.experimental_rerun()

def payment_screen():
    st.subheader("Payment Screen")

    if "booking_info" not in st.session_state:
        st.error("No booking information available.")
        return

    booking_info = st.session_state.booking_info

    st.text(f"Room No: {booking_info['room_no']}")
    st.text(f"Check-in Date: {booking_info['check_in_date']}")
    st.text(f"Check-out Date: {booking_info['check_out_date']}")
    st.text(f"Total Amount: ${booking_info['total_amount']:.2f}")

    payment_method = st.selectbox("Payment Method", ["UPI", "Netbanking", "Credit Card", "Debit Card"])

    if payment_method == "UPI":
        upi_id = st.text_input("UPI ID")
        if st.button("Confirm Payment"):
            process_payment("UPI", upi_id, booking_info)

    elif payment_method == "Netbanking":
        bank_name = st.text_input("Bank Name")
        account_number = st.text_input("Account Number")
        if st.button("Confirm Payment"):
            process_payment("Netbanking", f"{bank_name} {account_number}", booking_info)

    elif payment_method == "Credit Card":
        card_number = st.text_input("Card Number")
        card_expiry = st.text_input("Card Expiry Date (MM/YY)")
        card_cvv = st.text_input("Card CVV", type="password")
        if st.button("Confirm Payment"):
            process_payment("Credit Card", f"{card_number} {card_expiry} {card_cvv}", booking_info)

    elif payment_method == "Debit Card":
        card_number = st.text_input("Card Number")
        card_expiry = st.text_input("Card Expiry Date (MM/YY)")
        card_cvv = st.text_input("Card CVV", type="password")
        if st.button("Confirm Payment"):
            process_payment("Debit Card", f"{card_number} {card_expiry} {card_cvv}", booking_info)

def process_payment(method, details, booking_info):
    new_booking = Booking(
        user_id=booking_info['user_id'],
        room_no=booking_info['room_no'],
        check_in_date=booking_info['check_in_date'],
        check_out_date=booking_info['check_out_date'],
        total_amount=booking_info['total_amount']
    )
    session.add(new_booking)
    session.commit()

    new_payment = Payment(
        booking_id=new_booking.booking_id,
        payment_date=date.today(),
        amount=booking_info['total_amount'],
        payment_method=method
    )
    session.add(new_payment)
    session.commit()

    message_placeholder = st.empty()
    message_placeholder.success("Payment successful! Your booking is confirmed.")
    time.sleep(2)
    message_placeholder.empty()

    st.session_state.payment_stage = None
    st.session_state.task = "View Available Rooms"  # Redirect to home by resetting the task
    st.session_state.payment_done = True  # Mark payment done
    del st.session_state.booking_info
    st.experimental_rerun()