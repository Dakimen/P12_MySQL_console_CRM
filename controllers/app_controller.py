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
from services.sentry import SentryJournalisation


class AppContext:
    """
    Centralizes and initializes application dependencies.

    AppContext acts as the composition root of the application, responsible
    for creating and wiring together services, views, controllers, and
    cross-cutting infrastructure components. It ensures that all parts of
    the application receive the required dependencies and share a consistent
    context.
    """
    def __init__(self):
        """
        Initialize the application context and its dependencies.

        Instantiates core services, views, controllers, and infrastructure
        components, and injects the appropriate dependencies into each
        controller. This setup allows controllers to coordinate business
        logic, user interaction, and persistence concerns in a structured
        and maintainable way.
        """
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
    """
    Coordinates the high-level application flow.

    The AppController is responsible for initializing the application context
    and orchestrating the startup sequence. It verifies whether user login
    is required, triggers authentication-related actions, and delegates
    control to the main menu once authentication is complete.

    This class acts as the primary entry point for running the application
    and coordinating interactions between context-managed controllers.
    """

    def __init__(self):
        """
        Initialize the application controller.

        Creates and stores the application context, which provides access
        to the various controllers and shared resources required to run
        the application.
        """
        self.context = AppContext()

    def run(self):
        """
        Execute the main application workflow.

        Verifies whether user authentication is required. If login is
        successful or not required, retrieves the user's token and roles
        and displays the main menu.

        Returns:
            Any: The result of displaying the main menu, as returned by
            the menu controller, or None if login is not required or fails.
        """
        login_status = self.context.login_controller.verify_login_needed()
        if login_status:
            self.context.menu_controller.get_token_and_roles()
            return self.context.menu_controller.display_main_menu()
        else:
            return None
