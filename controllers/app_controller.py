from controllers.menu_controllers.login_controller import LoginMenuController
from controllers.menu_controllers.menu_controller import MenuController
from controllers.client_controller import ClientController
from controllers.contract_controller import ContractController
from controllers.event_controller import EventController
from controllers.collaborator_controller import CollaboratorController
from services.auth_service import AuthService
from services.client_service import ClientService
from services.event_service import EventService
from views.client_view import ClientView
from views.contract_view import ContractView
from services.contract_service import ContractService
from views.event_view import EventView
from views.collab_view import CollaboratorView
from services.collaborator_service import CollaboratorService
from sentry import SentryJournalisation


class AppContext:
    def __init__(self):
        self.sentry = SentryJournalisation()
        self.auth_service = AuthService()
        self.client_service = ClientService()
        self.contract_service = ContractService()
        self.client_view = ClientView()
        self.contract_view = ContractView()
        self.event_view = EventView()
        self.collab_view = CollaboratorView()
        self.event_service = EventService()
        self.collab_service = CollaboratorService()
        self.collab_controller = CollaboratorController(self.auth_service,
                                                        self.collab_view,
                                                        self.collab_service,
                                                        self.sentry)
        self.client_controller = ClientController(self.client_view,
                                                  self.client_service,
                                                  self.auth_service)
        self.contract_controller = ContractController(self.contract_view,
                                                      self.client_service,
                                                      self.auth_service,
                                                      self.contract_service,
                                                      self.sentry)
        self.login_controller = LoginMenuController(self.collab_controller,
                                                    self.auth_service,
                                                    self.collab_view)
        self.event_controller = EventController(self.event_view,
                                                self.auth_service,
                                                self.event_service,
                                                self.contract_service,
                                                self.contract_view)
        self.menu_controller = MenuController(self.auth_service,
                                              self.client_controller,
                                              self.contract_controller,
                                              self.event_controller,
                                              self.collab_controller)


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
