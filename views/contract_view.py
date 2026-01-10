from views.base_view import BaseView


class ContractView(BaseView):
    def get_client(self):
        client_name = self.prompt("Please enter client's name:")
        email = self.prompt("And his email:")
        return client_name, email

    def get_responsible(self):
        name = self.prompt(
            "Please enter the name of the commercial responsible:"
            )
        return name

    def get_date_created(self):
        return self.prompt_date(("Please enter the date of "
                                 "the contract's creation"))

    def get_signed(self):
        decision = self.prompt_choice(
            "Was the contract signed? Y/N",
            {"Y", "N"}
            )
        if decision == "Y":
            signed = self.prompt_date(("Please enter the date "
                                       "when the contract was signed"))
        else:
            signed = None
        return signed

    def get_created_signed(self):
        created = self.get_date_created()
        signed = self.get_signed()
        return created, signed

    def get_paid_not_exceeding_full(self, full):
        self.message("ATTENTION: The amount paid exceeds the full price")
        self.message(f"Please enter the amount paid not exceeding {full}")
        while True:
            paid = self.prompt_int("Please enter the amount paid:")
            if int(paid) > int(full):
                print("Amount exceeds full price. Try again.")
                continue
            return paid

    def get_contract_details(self):
        full = self.prompt_int("Please enter full amount agreed on:")
        paid = self.prompt_int("Please enter the amount paid:")
        if int(paid) > int(full):
            paid = self.get_paid_not_exceeding_full(full)
        return full, paid

    def display_contract_info(self, contract):
        self.section()
        self.labeled("Amount full", contract[0])
        self.labeled("Amount remaining", contract[1])
        self.labeled("Creation date", contract[2])
        if contract[3] is not None:
            self.labeled("Signed", contract[3])
        else:
            self.labeled("Signed", "No")
        self.labeled("Commercial responsible", contract[4])
        self.labeled("Client name", contract[5])
        self.end_section()
