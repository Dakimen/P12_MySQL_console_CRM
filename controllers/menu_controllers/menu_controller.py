from views.menu_view import Menu


class MenuController:
    """
    Manages all interactive menus and user navigation within the application.

    The MenuController is responsible for displaying menus, handling user
    input, enforcing role-based access control, and routing user actions
    to the appropriate domain controllers. It acts as the central dispatcher
    for all menu-driven workflows in the application.
    """
    def __init__(self, auth_service, client_controller,
                 contract_controller, event_controller,
                 collab_controller):
        """
            Initialize the menu controller and configure all menu definitions.

            Stores references to required services and controllers, initializes
            user authentication state, and defines the structure and behavior
            of all application menus and submenus.

            Args:
            auth_service: Service responsible for authentication.
            client_controller: Controller handling client-related actions.
            contract_controller: Controller handling contract-related actions.
            event_controller: Controller handling event-related actions.
            collab_controller: Controller handling collaborator-related actions
        """
        self.auth_service = auth_service
        self.client_controller = client_controller
        self.contract_controller = contract_controller
        self.event_controller = event_controller
        self.collab_controller = collab_controller
        self.user_token = None
        self.user_roles = None
        self.MAIN_MENU_OPTIONS = {
          "1": {"text": "Client Menu",
                "key": "1",
                "action": self.display_client_menu,
                "role": None
                },
          "2": {"text": "Contract Menu",
                "key": "2",
                "action": self.display_contract_menu,
                "role": None
                },
          "3": {"text": "Event Menu",
                "key": "3",
                "action": self.display_event_menu,
                "role": None
                },
          "4": {"text": "Collaborator Menu",
                "key": "4",
                "action": self.display_collaborator_menu,
                "role": None
                },
          "5": {"text": "Logout",
                "key": "5",
                "action": self.auth_service.logout,
                "role": None},
          "Q": {"text": "Quit programme",
                "key": "Q",
                "action": None,
                "role": None
                }
                }
        self.CLIENT_MENU_OPTIONS = {
            "1": {"text": "Display all clients",
                  "key": "1",
                  "action": self.client_controller.display_all_clients,
                  "role": None
                  },
            "2": {"text": "Find client",
                  "key": "2",
                  "action": self.find_client_router,
                  "role": None
                  },
            "3": {"text": "Add client",
                  "key": "3",
                  "action": self.client_controller.add_client,
                  "role": ["commercial responsible"]
                  },
            "4": {"text": "Update client info",
                  "key": "4",
                  "action": self.client_controller.update,
                  "role": ["commercial responsible"]
                  },
            "B": {"text": "Back to previous menu",
                  "key": "B",
                  "action": None,
                  "role": None
                  }
        }

        self.CLIENT_FILTER_OPTIONS = {
            "1": {"text": "Find using username",
                  "key": "1",
                  "action": self.client_controller.find_client_name},
            "2": {"text": "Find using email",
                  "key": "2",
                  "action": self.client_controller.find_client_email},
            "B": {"text": "Back to previous menu",
                  "key": "B",
                  "action": None}
        }

        self.CONTRACT_MENU_OPTIONS = {
            "1": {"text": "Display all contracts",
                  "key": "1",
                  "action": self.contract_controller.show_all,
                  "role": None
                  },
            "2": {"text": "Find contract",
                  "key": "2",
                  "action": self.contract_controller.find_contract,
                  "role": None
                  },
            "3": {"text": "Create contract",
                  "key": "3",
                  "action": self.contract_controller.add_contract,
                  "role": ["management responsible"]
                  },
            "4": {"text": "Modify contract",
                  "key": "4",
                  "action": self.find_contract_modif_router,
                  "role": ["management responsible", "commercial responsible"]
                  },
            "5": {"text": "Filter contracts",
                  "key": "5",
                  "action": self.find_contract_filter_router,
                  "role": ["commercial responsible"]
                  },
            "B": {"text": "Back to previous menu",
                  "key": "B",
                  "action": None,
                  "role": None
                  }
        }
        self.CONTRACT_FILTER_OPTIONS = {
            "1": {"text": "Filter by not signed",
                  "key": "1",
                  "action": self.contract_controller.filter_not_signed},
            "2": {"text": "Filter by not fully paid",
                  "key": "2",
                  "action": self.contract_controller.filter_not_paid},
            "B": {"text": "Back to previous menu",
                  "key": "B",
                  "action": None}
        }
        self.CONTRACT_MODIF_OPTIONS = {
            "1": {"text": "Sign contract",
                  "key": "1",
                  "action": self.contract_controller.sign_contract},
            "2": {"text": "Modify contract",
                  "key": "2",
                  "action": self.contract_controller.router_modif},
            "B": {"text": "Back to the previous menu",
                  "key": "B",
                  "action": None}
        }
        self.EVENT_MENU_OPTIONS = {
            "1": {"text": "Display all events",
                  "key": "1",
                  "action": self.event_controller.display_all,
                  "role": None
                  },
            "2": {"text": "Find event",
                  "key": "2",
                  "action": self.event_controller.find_event,
                  "role": None
                  },
            "3": {"text": "Create event",
                  "key": "3",
                  "action": self.event_controller.create_event,
                  "role": ["commercial responsible"]
                  },
            "4": {"text": "Modify event",
                  "key": "4",
                  "action": self.event_controller.modify_event,
                  "role": ["support responsible", "management responsible"]
                  },
            "5": {"text": "Filter events",
                  "key": "5",
                  "action": self.find_event_filter_router,
                  "role": ["support responsible", "management responsible"]
                  },
            "B": {"text": "Back to previous menu",
                  "key": "B",
                  "action": None,
                  "role": None
                  }
        }
        self.EVENT_FILTER_OPTIONS = {
            "1": {"text": "Display my events",
                  "key": "1",
                  "action": self.event_controller.filter_own_events,
                  "role": ["support responsible"]
                  },
            "2": {"text": "Display events without support",
                  "key": "2",
                  "action": self.event_controller.filter_no_support,
                  "role": ["management responsible"]
                  },
            "B": {"text": "Back to previous menu",
                  "key": "B",
                  "action": None,
                  "role": None
                  }
        }
        self.COLLAB_MENU_OPTIONS = {
            "1": {"text": "Change password",
                  "key": "1",
                  "action": self.collab_controller.change_password,
                  "role": None
                  },
            "2": {"text": "Display all collaborators",
                  "key": "2",
                  "action": self.collab_controller.get_all,
                  "role": ["management responsible"]
                  },
            "3": {"text": "Add collaborator",
                  "key": "3",
                  "action": self.collab_controller.add_collab,
                  "role": ["management responsible"]
                  },
            "4": {"text": "Modify collaborator",
                  "key": "4",
                  "action": self.find_collab_modif_router,
                  "role": ["management responsible"]
                  },
            "B": {"text": "Back to previous menu",
                  "key": "B",
                  "action": None,
                  "role": None
                  }
                  }
        self.COLLAB_MODIF_OPTIONS = {
            "1": {"text": "Modify collaborator's name",
                  "key": "1",
                  "action": self.collab_controller.modif_name,
                  "role": None
                  },
            "2": {"text": "Modify collaborator's email",
                  "key": "2",
                  "action": self.collab_controller.modif_email,
                  "role": None
                  },
            "3": {"text": "Assign role to collaborator",
                  "key": "3",
                  "action": self.collab_controller.assign_role,
                  "role": None
                  },
            "B": {"text": "Back to previous menu",
                  "key": "B",
                  "action": None,
                  "role": None
                  }
        }

    def display_main_menu(self):
        """
        Display the main application menu and handle user navigation.

        Continuously displays the main menu until the user chooses to quit
        the application. Each selected option triggers its associated action
        or submenu.
        """
        authorized_options = self.MAIN_MENU_OPTIONS
        main_menu = Menu('Main Menu', authorized_options)
        user_choice = main_menu.display_menu()
        action = authorized_options[user_choice]["action"]
        if action:
            action()
        while user_choice != "Q":
            user_choice = main_menu.display_menu()
            if user_choice == "Q":
                return None
            action = authorized_options[user_choice]["action"]
            if action:
                action()

    def display_client_menu(self):
        """
        Display the client management menu.

        Filters client menu options based on the user's roles and delegates
        navigation to the generic menu display handler.
        """
        authorized_options = self.get_authorized_menu_options(
            self.CLIENT_MENU_OPTIONS
            )
        self.display_menu('Client Menu', authorized_options)

    def find_client_router(self):
        """
        Display the client search submenu.

        Allows the user to select different client search strategies,
        such as searching by name or email.
        """
        self.display_menu("Client search", self.CLIENT_FILTER_OPTIONS)

    def display_contract_menu(self):
        """
        Display the contract management menu.

        Filters contract menu options according to the user's roles and
        routes user actions accordingly.
        """
        authorized_options = self.get_authorized_menu_options(
            self.CONTRACT_MENU_OPTIONS
            )
        self.display_menu('Contract Menu', authorized_options)

    def find_contract_filter_router(self):
        """
        Display the contract filtering submenu.

        Allows the user to apply predefined filters to contract listings,
        such as unsigned or unpaid contracts.
        """
        self.display_menu("Contract search", self.CONTRACT_FILTER_OPTIONS)

    def find_contract_modif_router(self):
        """
        Display the contract modification submenu.

        Provides options to sign or modify existing contracts based on
        user authorization.
        """
        self.display_menu("Contract modification", self.CONTRACT_MODIF_OPTIONS)

    def display_event_menu(self):
        """
        Display the event management menu.

        Filters event-related actions based on user roles and delegates
        execution to the selected event controller actions.
        """
        authorized_options = self.get_authorized_menu_options(
            self.EVENT_MENU_OPTIONS
            )
        self.display_menu('Event Menu', authorized_options)

    def find_event_filter_router(self):
        """
        Display the event filtering submenu.

        Allows authorized users to filter events, such as viewing assigned
        events or events without support staff.
        """
        authorized_options = self.get_authorized_menu_options(
            self.EVENT_FILTER_OPTIONS
            )
        self.display_menu('Event search', authorized_options)

    def display_collaborator_menu(self):
        """
        Display the collaborator management menu.

        Provides access to collaborator-related actions, such as listing,
        adding, or modifying collaborators, depending on user roles.
        """
        authorized_options = self.get_authorized_menu_options(
            self.COLLAB_MENU_OPTIONS
            )
        self.display_menu('Collaborator Menu', authorized_options)

    def find_collab_modif_router(self):
        """
        Display the collaborator modification submenu.

        Allows authorized users to update collaborator details such as
        name, email, or assigned roles.
        """
        authorized_options = self.get_authorized_menu_options(
            self.COLLAB_MODIF_OPTIONS
            )
        self.display_menu('Event search', authorized_options)

    def get_authorized_menu_options(self, menu_options):
        """
        Filter menu options based on the user's roles.

        Args:
            menu_options (dict): A dictionary of menu options containing
                role requirements.

        Returns:
            dict: A dictionary containing only the options the user is
            authorized to access.
        """
        authorized = {}

        for key, option in menu_options.items():
            roles = option["role"]
            if roles is None or any(self.has_role(role) for role in roles):
                authorized[key] = option

        return authorized

    def has_role(self, role: str) -> bool:
        """
        Check whether the current user has a specific role.

        Args:
            role (str): The role to verify.

        Returns:
            bool: True if the user has the role, False otherwise.
        """
        return self.user_token and role in self.user_roles

    def get_token_and_roles(self):
        """
        Retrieve and store the authenticated user's token and roles.

        Fetches the authentication token from temporary storage and resolves
        the associated user roles via the authentication service.
        """
        self.user_token = self.auth_service.get_token_from_temp()
        self.user_roles = self.auth_service.get_roles(self.user_token)

    @staticmethod
    def display_menu(menu_name, authorized_options):
        """
        Display a generic menu and execute selected actions.

        Continuously displays the given menu until the user chooses to
        return to the previous menu. Executes the action associated with
        each selected menu option.

        Args:
            menu_name (str): The title of the menu to display.
            authorized_options (dict): Menu options available to the user.
        """
        menu = Menu(menu_name, authorized_options)
        user_choice = menu.display_menu().upper()
        action = authorized_options[user_choice]["action"]
        if action:
            action()
        while user_choice != "B":
            user_choice = menu.display_menu()
            action = authorized_options[user_choice]["action"]
            if user_choice == "B":
                return None
            if action:
                action()
