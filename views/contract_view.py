from views.base_view import BaseView


class ContractView(BaseView):
    """
    Contract view class used for displaying contract information
    and collecting contract-related user input.

    Inherits from BaseView and relies on its helper methods for
    prompting, messaging, and formatted output.
    """
    def get_client(self):
        """
        Prompts user to enter client informations relevant to contract
        creation and updating.

        Returns:
            client_name(str): Entered name.
            email (str): Entered email.
        """
        client_name = self.prompt("Please enter client's name:")
        email = self.prompt("And his email:")
        return client_name, email

    def get_responsible(self):
        """
        Prompts user to enter commercial responsible's name.

        Returns:
            name (str): Entered name.
        """
        name = self.prompt(
            "Please enter the name of the commercial responsible:"
            )
        return name

    def get_date_created(self):
        """
        Prompts user to enter the date of the contract's creation.

        Returns:
            date (datetime): Entered date converted to a Datetime instance.
        """
        return self.prompt_date(("Please enter the date of "
                                 "the contract's creation"))

    def get_signed(self):
        """
        Prompts user to enter informations relating to a contract's signing.

        If signing is confirmed by user, they are prompted to enter contract's
        signature date.

        Returns:
            signed (datetime | None): Entered date if applicable.
        """
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
        """
        Prompts user to enter dates relevant to the contract.

        Returns:
            created (datetime): Entered date of contract's creation.
            signed (datetime | None): Entered signature date if applicable.
        """
        created = self.get_date_created()
        signed = self.get_signed()
        return created, signed

    def get_paid_not_exceeding_full(self, full):
        """
        Prompts user to enter a new paid value, by notifying them the previous
        exceeded the full contract's total.

        Args:
            full (str): A string containing an intable contract total.

        Returns:
            paid (str): A string numerical value not exceeding full.
        """
        self.message("ATTENTION: The amount paid exceeds the full price")
        self.message(f"Please enter the amount paid not exceeding {full}")
        while True:
            paid = self.prompt_int("Please enter the amount paid:")
            if int(paid) > int(full):
                print("Amount exceeds full price. Try again.")
                continue
            return paid

    def get_contract_details(self):
        """
        Prompts user to enter values relating to contract's total and paid
        amounts.
        Ensures paid does not exceed total price.

        Returns:
            full (str): A string numerical value representing contract's total.
            paid (str): Amount already paid not exceeding full.
        """
        full = self.prompt_int("Please enter full amount agreed on:")
        paid = self.prompt_int("Please enter the amount paid:")
        if int(paid) > int(full):
            paid = self.get_paid_not_exceeding_full(full)
        return full, paid

    def display_contract_info(self, contract):
        """
        Display a contract's information in a formatted section.

        Args:
            contract (tuple | list): Contract data containing:
                (full amount, amount remaining, creation date, signature date,
                commercial responsible and client's name).

        Side Effects:
            - Outputs formatted contract information to the user interface.
        """
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
