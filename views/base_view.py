from abc import ABC
from datetime import datetime
import getpass


class BaseView(ABC):
    SEPARATOR = "=" * 20

    def message(self, text: str):
        print(text)

    def section(self):
        print("\n" + self.SEPARATOR)

    def end_section(self):
        print(self.SEPARATOR)

    def labeled(self, label: str, value):
        if value is not None:
            print(f"{label}: {value}")

    def prompt(self, text: str) -> str:
        print(text)
        return input(">>> ")

    def prompt_password(self, text: str) -> str:
        print(text)
        return getpass.getpass()

    def prompt_int(self, text: str) -> int:
        while True:
            value = self.prompt(text)
            try:
                return int(value)
            except ValueError:
                print("Please enter a valid number.")

    def prompt_choice(self, text: str, choices: set[str]) -> str:
        while True:
            value = self.prompt(text).upper()
            if value in choices:
                return value
            print(f"Please choose one of {', '.join(choices)}")

    def prompt_date(self, text: str, fmt="%d/%m/%Y") -> datetime:
        while True:
            text = f"{text}\n Please use the following format {fmt}"
            value = self.prompt(text)
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                print(f"Invalid date. Use format {fmt}")
