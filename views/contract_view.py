import re


class ContractView():
    def __init__(self):
        self.dateformat = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
        self.monetary_format = r"^[0-9]+$"

    def contract_created(self):
        print("Contract added successfully!")

    def something_went_wrong(self):
        print("Something went wrong, try again")

    def get_client(self):
        print("To add contract please enter client's name:")
        client_name = input(">>> ")
        print("And his email:")
        email = input(">>> ")
        return client_name, email

    def get_date_created(self):
        print("Please enter the date of the contract's creation")
        date = ""
        while not re.match(self.dateformat, date):
            print("Follow the following format: dd/mm/yyyy")
            date = input(">>> ")
        return date

    def get_date_signed(self):
        print("Please enter the date when the contract was signed")
        date = ""
        while not re.match(self.dateformat, date):
            print("Follow the following format: dd/mm/yyyy")
            date = input(">>> ")
        return date

    def get_contract_details(self):
        print("Please enter full amount agreed on:")
        full = ""
        while not re.match(self.monetary_format, full):
            print("Please enter only numbers, ex: 6500")
            full = input(">>> ")
        print("Please enter the amount paid:")
        paid = ""
        while not re.match(self.monetary_format, paid):
            print("Please enter only numbers, ex: 6500")
            paid = input(">>> ")
        created = self.get_date_created()
        decision = False
        while decision is False:
            print("Was the contract signed? Y/N")
            user_input = input(">>> ")
            if user_input == "Y" or user_input == "N":
                decision = True
        if user_input == "Y":
            signed = self.get_date_signed()
        else:
            signed = None
        return full, paid, created, signed
