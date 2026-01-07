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

    def get_sum(self):
        amount = ""
        while not re.match(self.monetary_format, amount):
            print("Please enter only numbers, ex: 6500")
            amount = input(">>> ")
        return amount

    def get_signed(self):
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
        return signed

    def get_paid_not_exceeding_full(self, full):
        print("ATTENTION: The amount paid exceeds the full price")
        print(f"Please enter the amount paid not exceeding {full}")
        while True:
            paid = input(">>> ")

            if not re.fullmatch(self.monetary_format, paid):
                print("Please enter only numbers")
                continue

            if int(paid) > int(full):
                print("Amount exceeds full price. Try again.")
                continue
            return paid

    def get_contract_details(self):
        print("Please enter full amount agreed on:")
        full = self.get_sum()
        print("Please enter the amount paid:")
        paid = self.get_sum()
        if int(paid) > int(paid):
            paid = self.get_paid_not_exceeding_full(full)
        created = self.get_date_created()
        signed = self.get_signed()
        return full, paid, created, signed

    def display_contract_info(self, contract):
        print("\n")
        print("====================")
        print(f"Amount full: {contract[0]}")
        print(f"Amount remaining: {contract[1]}")
        print(f"Creation date: {contract[2]}")
        if contract[3] is not None:
            print(f"Signed: {contract[3]}")
        else:
            print("Signed: No")
        print(f"Commercial Responsible: {contract[4]}")
        print(f"Client name: {contract[5]}")
        print("====================")
