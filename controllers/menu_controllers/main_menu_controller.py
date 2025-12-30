from views.menu_view import Menu
from controllers.user_controller import UserController
from controllers.menu_controllers.commercial_menu_controller import CommercialMenuController
from controllers.menu_controllers.management_menu_controller import ManagementMenuController
from controllers.menu_controllers.support_menu_controller import SupportMenuController


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
                user = action()
                if user:
                    self.determine_role(user)
        return None

    def determine_role(self, user):
        role = user["role"]

        role_menu_map = {
            "management": ManagementMenuController,
            "commercial": CommercialMenuController,
            "support": SupportMenuController
        }

        controller_class = role_menu_map.get(role)

        if not controller_class:
            raise ValueError(f"Unknown role: {role}")

        controller = controller_class()
        controller.display()
