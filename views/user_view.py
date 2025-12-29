import getpass
import bcrypt


class UserView:
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

    def account_created_info():
        print("Your account has been created "
              "and now awaits management approval and role assignation.")
        return None

    def connection_success():
        print("Connection success!")
        return None

    def connection_failure():
        print("Connection unsuccessful or the account wasn't approved yet!")
