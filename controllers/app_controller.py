from controllers.menu_controllers.login_menu_controller import LoginMenuController
from controllers.menu_controllers.main_menu_controller import MainMenuController


class AppContext:

    def __init__(self):
        self.login_controller = LoginMenuController()
        self.menu_controller = MainMenuController()

    def run(self):
        user = self.login_controller.verify_login_needed()
        if user:
            return self.menu_controller.main_menu(user)
        else:
            return None
