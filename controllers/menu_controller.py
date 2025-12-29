from views.menu_view import Menu
from models.user_model import User, find_user


class MenuController:

    def __init__(self):
        self.menu = Menu

    def main_menu(self):
        user_choice = self.menu.main_menu_view()
        if user_choice == "1":
            return self.login_controller()
        if user_choice == "2":
            return self.user_creation_controller()

    def user_creation_controller(self):
        email, name, pass_hush = self.menu.add_user_view()
        user = User(email, name, pass_hush)
        user.save_user_to_db()
        return self.main_menu()

    def login_controller(self):
        email, password = self.menu.login_view()
        token, name, password_hush = find_user(email, password)
        if token is False:
            print("Connection failed!")
        else:
            user_account = User(email, name, password_hush, token=token)
            return None
