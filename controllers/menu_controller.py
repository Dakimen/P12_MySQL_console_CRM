from views.menu_view import Menu
from controllers.user_controller import UserController


class MenuController:

    def __init__(self):
        self.user_controller = UserController()
        self.MAIN_MENU_OPTIONS = {
            "1": {"text": "Log-in to an existing account",
                  "key": "1",
                  "action": self.user_controller.login_controller},
            "2": {"text": "Create an account",
                  "key": "2",
                  "action": self.user_controller.user_creation_controller},
            "Q": {"text": "Quit programme",
                  "key": "Q",
                  "action": None}
                  }

    def main_menu(self):
        main_menu = Menu('Main menu', self.MAIN_MENU_OPTIONS)
        user_choice = main_menu.display_menu()
        action = self.MAIN_MENU_OPTIONS[user_choice]["action"]
        if action:
            action()
        while user_choice != "Q" and user_choice != "q":
            user_choice = main_menu.display_menu()
            if user_choice == "q" or user_choice == "Q":
                return None
            action = self.MAIN_MENU_OPTIONS[user_choice]["action"]
            if action:
                action()
        return None

    def management_menu():
        pass

    def commercial_menu():
        pass
