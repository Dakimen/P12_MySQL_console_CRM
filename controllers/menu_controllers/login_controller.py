from views.menu_view import Menu


class LoginMenuController:

    def __init__(self, collab_controller, auth_service, user_view):
        self.collab_controller = collab_controller
        self.auth_service = auth_service
        self.user_view = user_view
        self.LOGIN_MENU_OPTIONS = {
            "1": {"text": "Log-in to an existing account",
                  "key": "1",
                  "action": self.login_controller},
            "Q": {"text": "Quit programme",
                  "key": "Q",
                  "action": None}
                  }

    def verify_login_needed(self):
        token = self.auth_service.get_token_from_temp()
        if token is None:
            return self.main_login_menu()
        elif self.auth_service.is_jwt_valid(token):
            return True
        else:
            self.auth_service.clean_json_temp("temp.json")
            return self.main_login_menu()

    def main_login_menu(self):
        main_menu = Menu('Login menu', self.LOGIN_MENU_OPTIONS)
        user_choice = main_menu.display_menu().upper()
        action = self.LOGIN_MENU_OPTIONS[user_choice]["action"]
        if action:
            return action()
        while user_choice != "Q":
            user_choice = main_menu.display_menu()
            if user_choice == "Q":
                return None
            action = self.LOGIN_MENU_OPTIONS[user_choice]["action"]
            if action:
                return action()

    def login_controller(self):
        email, password = self.user_view.login_view()
        user_id, roles = self.collab_controller.find_user_by_email(email,
                                                                   password)
        if not user_id:
            self.user_view.message("Connection unsuccessful!")
        else:
            token = self.auth_service.generate_web_token(user_id, roles)
            self.auth_service.write_token_to_temp(token)
            return True
        return False
