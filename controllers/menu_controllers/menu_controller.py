from views.menu_view import Menu


class MenuController:
    def __init__(self, auth_service, client_controller):
        self.auth_service = auth_service
        self.client_controller = client_controller
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
                  "role": ["management responsible"]
                  },
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
                  "action": self.display_main_menu,
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
                  "action": None,
                  "role": None
                  },
            "2": {"text": "Find contract",
                  "key": "2",
                  "action": None,
                  "role": None
                  },
            "3": {"text": "Create contract",
                  "key": "3",
                  "action": None,
                  "role": ["management responsible"]
                  },
            "4": {"text": "Modify contract",
                  "key": "4",
                  "action": None,
                  "role": ["management responsible", "commercial responsible"]
                  },
            "5": {"text": "Filter contracts",
                  "key": "5",
                  "action": None,
                  "role": ["commercial responsible"]
                  },
            "B": {"text": "Back to previous menu",
                  "key": "B",
                  "action": self.display_main_menu,
                  "role": None
                  }
        }
        self.EVENT_MENU_OPTIONS = {
            "1": {"text": "Display all events",
                  "key": "1",
                  "action": None,
                  "role": None
                  },
            "2": {"text": "Find event",
                  "key": "2",
                  "action": None,
                  "role": None
                  },
            "3": {"text": "Create event",
                  "key": "3",
                  "action": None,
                  "role": ["commercial responsible"]
                  },
            "4": {"text": "Modify event",
                  "key": "4",
                  "action": None,
                  "role": ["support responsible", "management responsible"]
                  },
            "5": {"text": "Filter events",
                  "key": "5",
                  "action": None,
                  "role": ["support responsible", "management responsible"]
                  },
            "B": {"text": "Back to previous menu",
                  "key": "B",
                  "action": self.display_main_menu,
                  "role": None
                  }
        }
        self.COLLAB_MENU_OPTIONS = {
            "1": {"text": "Display all collaborators",
                  "key": "1",
                  "action": None
                  },
            "2": {"text": "Find collaborator",
                  "key": "2",
                  "action": None
                  },
            "3": {"text": "Add collaborator",
                  "key": "3",
                  "action": None
                  },
            "4": {"text": "Modify collaborator",
                  "key": "4",
                  "action": None
                  },
            "5": {"text": "Delete collaborator",
                  "key": "5",
                  "action": None
                  },
            "B": {"text": "Back to previous menu",
                  "key": "B",
                  "action": self.display_main_menu
                  }
        }

    def display_main_menu(self):
        authorized_options = self.get_authorized_menu_options(
            self.MAIN_MENU_OPTIONS
            )
        main_menu = Menu('Main Menu', authorized_options)
        user_choice = main_menu.display_menu()
        action = authorized_options[user_choice]["action"]
        if action:
            return action()
        while user_choice != "Q":
            user_choice = main_menu.display_menu()
            if user_choice == "Q":
                return None
            action = authorized_options[user_choice]["action"]
            if action:
                action()

    def display_client_menu(self):
        authorized_options = self.get_authorized_menu_options(
            self.CLIENT_MENU_OPTIONS
            )
        self.display_menu('Client Menu', authorized_options)

    def find_client_router(self):
        self.display_menu("Client search", self.CLIENT_FILTER_OPTIONS)

    def display_contract_menu(self):
        authorized_options = self.get_authorized_menu_options(
            self.CONTRACT_MENU_OPTIONS
            )
        self.display_menu('Contract Menu', authorized_options)

    def display_event_menu(self):
        authorized_options = self.get_authorized_menu_options(
            self.EVENT_MENU_OPTIONS
            )
        self.display_menu('Event Menu', authorized_options)

    def display_collaborator_menu(self):
        authorized_options = self.get_authorized_menu_options(
            self.COLLAB_MENU_OPTIONS
            )
        self.display_menu('Collaborator Menu', authorized_options)

    def get_authorized_menu_options(self, menu_options):
        authorized = {}

        for key, option in menu_options.items():
            roles = option["role"]
            if roles is None or any(self.has_role(role) for role in roles):
                authorized[key] = option

        return authorized

    def has_role(self, role: str) -> bool:
        return self.user_token and role in self.user_roles

    def get_token_and_roles(self):
        self.user_token = self.auth_service.get_token_from_temp()
        self.user_roles = self.auth_service.get_roles(self.user_token)

    @staticmethod
    def display_menu(menu_name, authorized_options):
        menu = Menu(menu_name, authorized_options)
        user_choice = menu.display_menu()
        action = authorized_options[user_choice]["action"]
        if action:
            action()
        while user_choice != "B":
            user_choice = menu.display_menu()
            action = authorized_options[user_choice]["action"]
            if user_choice == "B":
                if action is not None:
                    return action()
                else:
                    return None
            if action:
                action()
