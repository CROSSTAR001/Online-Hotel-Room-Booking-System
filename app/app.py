import streamlit as st
from auth import login_user, signup_user, login_admin, signup_admin
from users import user_dashboard, payment_screen
from admins import admin_dashboard
from database import session, User, Admin
import base64

# Convert your image to base64
with open("room.jpg", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode()

# Set page configuration
st.set_page_config(
    page_title="Hotel Room Booking System",
    page_icon="logo.png",  # You can use an emoji or provide the path to your favicon
    layout="wide"
)

def main():
    # Adding a background image with reduced opacity using custom CSS
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), url("data:image/jpg;base64,{base64_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: black !important;
        }}
        .stApp header, .stApp footer, .stApp .css-10trblm {{
            background: transparent !important;
            color: black !important;
        }}
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp div, .stApp span, .stApp label {{
            color: black !important;
        }}
        .stMarkdown, .stText, .stTitle, .stSubheader, .stCaption, .stSidebar .stSelectbox label {{
            color: black !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Hotel Room Booking System")

    if "payment_stage" not in st.session_state:
        st.session_state.payment_stage = None

    if "user" not in st.session_state:
        st.session_state.user = None

    if "admin" not in st.session_state:
        st.session_state.admin = None

    if st.session_state.payment_stage == "payment":
        payment_screen()
    else:
        menu = ["Home", "Login", "Sign Up"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Home":
            st.subheader("Home")
            st.markdown("**Welcome to the Hotel Room Booking System**")

        elif choice == "Login":
            st.subheader("Login Section")

            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type='password')
            user_type = st.sidebar.radio("Login as", ("User", "Admin"))

            if st.sidebar.button("Login"):
                if user_type == "User":
                    user = login_user(username, password)
                    if user:
                        st.success(f"Logged in as {user.name}")
                        st.session_state.user = user
                        st.experimental_rerun()
                    else:
                        st.warning("Incorrect Username/Password")
                else:
                    admin = login_admin(username, password)
                    if admin:
                        st.success(f"Logged in as {admin.name}")
                        st.session_state.admin = admin
                        st.experimental_rerun()
                    else:
                        st.warning("Incorrect Username/Password")

        elif choice == "Sign Up":
            st.subheader("Create New Account")
            user_type = st.radio("Sign up as", ("User", "Admin"))

            if user_type == "User":
                name = st.text_input("Name")
                username = st.text_input("Username")
                password = st.text_input("Password", type='password')
                email = st.text_input("Email")
                phone_no = st.text_input("Phone Number")
                address = st.text_area("Address")

                if st.button("Sign Up"):
                    signup_user(name, username, password, email, phone_no, address)
                    st.success("You have successfully created an account")
                    st.info("Go to the Login menu to login")

            else:
                name = st.text_input("Name")
                username = st.text_input("Username")
                password = st.text_input("Password", type='password')

                if st.button("Sign Up"):
                    signup_admin(name, username, password)
                    st.success("You have successfully created an account")
                    st.info("Go to the Login menu to login")

        if st.session_state.user:
            user_dashboard(st.session_state.user)
        elif st.session_state.admin:
            admin_dashboard(st.session_state.admin)

if __name__ == '__main__':
    main()
