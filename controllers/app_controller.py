from controllers.menu_controllers.login_controller import LoginMenuController
from controllers.menu_controllers.menu_controller import MenuController
from controllers.user_controller import UserController
from controllers.client_controller import ClientController
from controllers.auth_controller import AuthService
from views.user_view import UserView
from views.client_view import ClientView


class AppContext:
    def __init__(self):
        self.auth_service = AuthService()
        self.client_view = ClientView()
        self.user_view = UserView()
        self.user_controller = UserController(self.user_view,
                                              self.auth_service)
        self.client_controller = ClientController(self.client_view)
        self.login_controller = LoginMenuController(self.user_controller,
                                                    self.auth_service,
                                                    self.user_view)
        self.menu_controller = MenuController(self.auth_service,
                                              self.client_controller)


class AppController:

    def __init__(self):
        self.context = AppContext()

    def run(self):
        login_status = self.context.login_controller.verify_login_needed()
        if login_status:
            self.context.menu_controller.get_token_and_roles()
            return self.context.menu_controller.display_main_menu()
        else:
            return None
