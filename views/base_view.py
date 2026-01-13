from abc import ABC
from datetime import datetime
import getpass


class BaseView(ABC):
    """
    Abstract Base View class defining methods for all view classes.

    Such as displaying a message, maintaining a certain consistent style
    of sections for display and prompting user.
    """
    SEPARATOR = "=" * 20

    def message(self, text: str):
        """
        Prints out text passed to it.

        Args:
            text (str): Text to display.
        """
        print(text)

    def section(self):
        """
        Prints out a beginning separator for consistent section design.
        """
        print("\n" + self.SEPARATOR)

    def end_section(self):
        """
        Prints out an end separator for consistent section design.
        """
        print(self.SEPARATOR)

    def labeled(self, label: str, value):
        """
        Displays a labelled value.

        Args:
            label (str): Label to display next to the value.
            value (str): Value to display.
        """
        if value is not None:
            print(f"{label}: {value}")

    def prompt(self, text: str) -> str:
        """
        Prompts user input.

        Args:
            text (str): Prompt used to inform user which value to type.

        Returns:
            (str): User's input.
        """
        print(text)
        return input(">>> ")

    def prompt_password(self, text: str) -> str:
        """
        Prompts user to enter their password with getpass.

        Args:
            text (str): Prompt to display.

        Returns:
            user's password (str): User's password input.
        """
        print(text)
        return getpass.getpass()

    def prompt_int(self, text: str) -> int:
        """
        Prompts user to enter a numerical value.
        Loops as long as user's input is not an entire number.

        Args:
            text (str): Prompt to display.

        Returns:
            user's input (int): A numerical value.
        """
        while True:
            value = self.prompt(text)
            try:
                return int(value)
            except ValueError:
                print("Please enter a valid number.")

    def prompt_choice(self, text: str, choices: set[str]) -> str:
        """
        Prompts user to choose between proposed options.
        Loops until user chooses a valid option.

        Args:
            text (str): Prompt to display.
            choices (set[str]): List of choices to select from.

        Returns:
            user's choice (str): User's choice.
        """
        while True:
            value = self.prompt(text).upper()
            if value in choices:
                return value
            print(f"Please choose one of {', '.join(choices)}")

    def prompt_date(self, text: str, fmt="%d/%m/%Y") -> datetime:
        """
        Prompts user to enter a date conforming to a passed format.
        Loops until user enter's a value conforming to the format.

        Args:
            text (str): Prompt to display.
            fmt (str): Datetime format to enforce, default: %d/%m/%Y.

        Returns:
            created datetime (datetime).
        """
        while True:
            text = f"{text}\n Please use the following format {fmt}"
            value = self.prompt(text)
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                print(f"Invalid date. Use format {fmt}")
