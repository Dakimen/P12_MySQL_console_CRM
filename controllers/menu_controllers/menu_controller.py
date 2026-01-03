from views.menu_view import Menu


class MenuController:
    def __init__(self):
        self.user_token = None
        self.MAIN_MENU_OPTIONS = {
            "1": {"text": "Client Menu",
                  "key": "1",
                  "action": self.display_client_menu},
            "2": {"text": "Contract Menu",
                  "key": "2",
                  "action": self.display_contract_menu},
            "3": {"text": "Event Menu",
                  "key": "3",
                  "action": self.display_event_menu},
            "4": {"text": "Collaborator Menu",
                  "key": "4",
                  "action": self.display_collaborator_menu}
        }

    def display_main_menu(self):
        main_menu = Menu('Main Menu', self.MAIN_MENU_OPTIONS)
        user_choice = main_menu.display_menu()
        action = self.MAIN_MENU_OPTIONS[user_choice]["action"]
        if action:
            return action()
        while user_choice != "Q" and user_choice != "q":
            user_choice = main_menu.display_menu()
            if user_choice == "q" or user_choice == "Q":
                return None
            action = self.MAIN_MENU_OPTIONS[user_choice]["action"]
            if action:
                return action()

    def display_client_menu(self):
        pass

    def display_contract_menu(self):
        pass

    def display_event_menu(self):
        pass

    def display_collaborator_menu(self):
        pass
