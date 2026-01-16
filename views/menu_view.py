class Menu:
    """
    Menu class responsible for displaying multiple-choice menus
    and collecting user selections.
    """

    def __init__(self, menu_name, options):
        """
        Initialize a menu.

        Args:
            menu_name (str): Title displayed at the top of the menu.
            options (dict): Authorized menu options.
                Format:
                {
                    "1": {
                        "text": "Display all contracts",
                        "action": callable,
                        "role": None
                    },
                    "B": {
                        "text": "Back to previous menu",
                        "action": None,
                        "role": None
                    }
                }
        """
        self.menu_name = menu_name
        self.options = options

    def display_menu(self):
        """
        Display menu options and prompt user for a choice.

        Numeric options are displayed as 1, 2, 3, ...
        The 'B' (Back) option is always displayed last.

        Returns:
            str: The REAL option key selected by the user.
        """
        print()
        print(self.menu_name)

        numeric_options = []
        back_option = None

        for key, option in self.options.items():
            if key == "B" or key == "Q":
                back_option = (key, option)
            else:
                numeric_options.append((key, option))

        display_map = {}

        for index, (real_key, option) in enumerate(numeric_options, start=1):
            print(f"{index}: {option['text']}")
            display_map[str(index)] = real_key

        if back_option:
            if back_option[0] == "Q":
                print("Q: Quit programme")
                display_map["Q"] = "Q"
            elif back_option[0] == "B":
                print("B: Back to previous menu")
                display_map["B"] = "B"

        while True:
            user_choice = input(">>> ").upper()
            if user_choice in display_map:
                return display_map[user_choice]
            print("Please insert a valid option.")
