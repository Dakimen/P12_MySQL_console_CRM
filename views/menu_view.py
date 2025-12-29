import getpass
import bcrypt


class Menu:
    def __init__(self):
        pass

    def main_menu_view():
        AVAILABLE_CHOICES = ["1", "2"]
        print("EPIC EVENTS Application")
        print("Choose option:")
        print("1. Log-in to an existing account.")
        print("2. Create account.")
        user_choice = input(">>> ")
        while user_choice not in AVAILABLE_CHOICES:
            print('Choose an existant option:')
            user_choice = input(">>> ")
        return user_choice

    def add_user_view():
        print("User sign-up")
        print("Please enter following information:")
        print("Email:")
        login_email = input(">>> ")
        print("Username:")
        name = input(">>> ")
        password = getpass.getpass()
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return login_email, name, password_hash

    def login_view():
        print("Login.")
        print("Please enter your email:")
        email = input(">>> ")
        password = getpass.getpass()
        return email, password
