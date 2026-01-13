class Menu:
    """
    Menu class responsible for displaying multiple-choice menus
    and collecting user selections.
    """
    def __init__(self, menu_name, options):
        """
        Initialize a menu with a title and selectable options.

        Args:
            menu_name (str): The title displayed at the top of the menu.
            options (dict): A dictionary defining menu options.
                Each key maps to a dictionary with:
                    - "text" (str): Description of the option.
                    - "key" (str): Key the user must press to select
                       the option.

                Example:
                    {
                        "option1": {"text": "Create client", "key": "C"},
                        "option2": {"text": "Quit", "key": "Q"}
                    }

        Side Effects:
            - Builds internal lists of option texts and accepted keys.
            - Adds a lowercase 'q' as an accepted key when 'Q' is present.
        """
        self.options = []
        self.option_keys = []
        for key in options:
            self.options.append(options[key]["text"])
            self.option_keys.append(options[key]["key"])
            if options[key]["key"] == "Q":
                self.option_keys.append("q")
        self.menu_name = menu_name

    def display_menu(self):
        """
        Display the menu options and prompt the user for a choice.

        The prompt repeats until the user enters a valid option key.

        Returns:
            str: The selected menu option key in uppercase.
        """
        print("")
        print((
           f"{self.menu_name}"
           ))
        ticker = 0
        for option in self.options:
            print(f"{self.option_keys[ticker]}: {option}")
            ticker = ticker + 1
        user_choice = input(">>> ").upper()
        while user_choice not in self.option_keys:
            print("Please insert a valid option")
            user_choice = input(">>> ")
        return user_choice
