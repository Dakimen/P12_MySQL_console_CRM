from controllers.menu_controllers.login_controller import LoginMenuController
from controllers.menu_controllers.menu_controller import MenuController
from controllers.user_controller import UserController
from controllers.auth_controller import AuthService
from views.user_view import UserView


class AppContext:
    def __init__(self):
        self.user_view = UserView()
        self.menu_controller = MenuController()
        self.user_controller = UserController()
        self.auth_service = AuthService()
        self.login_controller = LoginMenuController(self.user_controller,
                                                    self.auth_service,
                                                    self.user_view)


class AppController:

    def __init__(self):
        self.context = AppContext()

    def run(self):
        login_status = self.context.login_controller.verify_login_needed()
        if login_status:
            return self.context.menu_controller.display_main_menu()
        else:
            return None
