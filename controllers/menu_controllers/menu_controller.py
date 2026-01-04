from views.menu_view import Menu


class MenuController:
    def __init__(self, auth_service):
        self.auth_service = auth_service
        self.user_token = None
        self.user_roles = None
        self.MAIN_MENU_OPTIONS = {
            "1": {"text": "Client Menu",
                  "key": "1",
                  "action": self.display_client_menu,
                  "role": None},
            "2": {"text": "Contract Menu",
                  "key": "2",
                  "action": self.display_contract_menu,
                  "role": None},
            "3": {"text": "Event Menu",
                  "key": "3",
                  "action": self.display_event_menu,
                  "role": None},
            "4": {"text": "Collaborator Menu",
                  "key": "4",
                  "action": self.display_collaborator_menu,
                  "role": "management responsible"},
            "Q": {"text": "Quit programme",
                  "key": "Q",
                  "action": None,
                  "role": None}
        }

    def display_main_menu(self):
        authorized_options = self.get_authorized_menu_options(
            self.MAIN_MENU_OPTIONS
            )
        main_menu = Menu('Main Menu', authorized_options)
        user_choice = main_menu.display_menu().upper()
        action = authorized_options[user_choice]["action"]
        if action:
            return action()
        while user_choice != "Q":
            user_choice = main_menu.display_menu()
            if user_choice == "Q":
                return None
            action = authorized_options[user_choice]["action"]
            if action:
                return action()

    def display_client_menu(self):
        pass

    def display_contract_menu(self):
        print("contract menu")

    def display_event_menu(self):
        print("event menu")

    def display_collaborator_menu(self):
        print("collaborator menu")

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
