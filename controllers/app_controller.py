from controllers.menu_controllers.login_controller import LoginMenuController
from controllers.menu_controllers.menu_controller import MenuController
from controllers.user_controller import UserController
from controllers.client_controller import ClientController
from controllers.contract_controller import ContractController
from controllers.event_controller import EventController
from services.auth_service import AuthService
from services.client_service import ClientService
from services.event_service import EventService
from views.user_view import UserView
from views.client_view import ClientView
from views.contract_view import ContractView
from services.contract_service import ContractService
from views.event_view import EventView


class AppContext:
    def __init__(self):
        self.auth_service = AuthService()
        self.client_service = ClientService()
        self.contract_service = ContractService()
        self.client_view = ClientView()
        self.user_view = UserView()
        self.contract_view = ContractView()
        self.event_view = EventView()
        self.event_service = EventService()
        self.user_controller = UserController(self.user_view,
                                              self.auth_service)
        self.client_controller = ClientController(self.client_view,
                                                  self.client_service,
                                                  self.auth_service)
        self.contract_controller = ContractController(self.contract_view,
                                                      self.client_service,
                                                      self.auth_service,
                                                      self.contract_service)
        self.login_controller = LoginMenuController(self.user_controller,
                                                    self.auth_service,
                                                    self.user_view)
        self.event_controller = EventController(self.event_view,
                                                self.auth_service,
                                                self.event_service,
                                                self.contract_service,
                                                self.contract_view)
        self.menu_controller = MenuController(self.auth_service,
                                              self.client_controller,
                                              self.contract_controller,
                                              self.event_controller)


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
