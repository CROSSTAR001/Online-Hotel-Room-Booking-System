from database import session, User, Admin

def login_user(username, password):
    user = session.query(User).filter(User.username == username, User.password == password).first()
    return user

def signup_user(name, username, password, email, phone_no, address):
    new_user = User(name=name, username=username, password=password, email=email, phone_no=phone_no, address=address)
    session.add(new_user)
    session.commit()

def login_admin(username, password):
    admin = session.query(Admin).filter(Admin.username == username, Admin.password == password).first()
    return admin

def signup_admin(name, username, password):
    new_admin = Admin(name=name, username=username, password=password)
    session.add(new_admin)
    session.commit()
