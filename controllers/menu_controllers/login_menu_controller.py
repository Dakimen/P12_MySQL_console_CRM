import json

from views.menu_view import Menu
from controllers.user_controller import UserController
from controllers.auth_controller import AuthService
from controllers.user_controller import User


class LoginMenuController:

    def __init__(self):
        self.user_controller = UserController()
        self.auth_service = AuthService()
        self.MAIN_MENU_OPTIONS = {
            "1": {"text": "Log-in to an existing account",
                  "key": "1",
                  "action": self.user_controller.login_controller},
            "Q": {"text": "Quit programme",
                  "key": "Q",
                  "action": None}
                  }

    def verify_login_needed(self):
        temp_storage = 'temp.json'
        try:
            with open(temp_storage, 'r') as file:
                data = json.load(file)
                token = data['token']
            if self.auth_service.is_jwt_valid(token):
                user_id = self.auth_service.get_user_id_from_token(token)
                email, name, hush = self.user_controller.find_user_by_id(user_id)
                user_account = User(email, name, hush, user_id, token)
                return user_account
            else:
                with open(temp_storage, 'w') as file:
                    json.dump({}, file)
                return self.main_login_menu()
        except FileNotFoundError:
            return self.main_login_menu()

    def main_login_menu(self):
        main_menu = Menu('Main menu', self.MAIN_MENU_OPTIONS)
        user_choice = main_menu.display_menu()
        action = self.MAIN_MENU_OPTIONS[user_choice]["action"]
        if action:
            return action()
        while user_choice != "Q" and user_choice != "q":
            user_choice = main_menu.display_menu()
            if user_choice == "q" or user_choice == "Q":
                return None
            action = self.MAIN_MENU_OPTIONS[user_choice]["action"]
            if action:
                return action()
