from views.base_view import BaseView


class ClientView(BaseView):
    """
    Client view class used for displaying client information
    and collecting client-related user input.

    Inherits from BaseView and relies on its helper methods for
    prompting, messaging, and formatted output.
    """
    def display_client(self, client):
        """
        Display a client's information in a formatted section.

        Args:
            client (tuple | list): Client data containing:
                (full_name, email, phone_number, company_name,
                 date_created[, last_updated]).

        Side Effects:
            - Outputs formatted client information to the user interface.
        """
        self.section()
        self.labeled("Name", client[0])
        self.labeled("Email", client[1])
        self.labeled("Phone number", client[2])
        self.labeled("Company name", client[3])
        self.labeled("Date created", client[4])
        try:
            self.labeled("Last updated", client[5])
        except IndexError:
            self.labeled("Last updated", client[4])
        self.end_section()

    def get_client_search_key(self, keyword):
        """
        Prompt the user to enter a search value for a client.

        Args:
            keyword (str): The client attribute to search by
                (e.g., "name", "email").

        Returns:
            str: The user-provided search value.
        """
        return self.prompt(f"Please enter client's {keyword}")

    def get_info_client(self):
        """
        Prompt the user to enter information for a new client.

        This includes full name, email, phone number, and
        optional company name.

        Returns:
            tuple: A tuple containing:
                (full_name, email, phone_number, company_name),
                where company_name may be None.
        """
        full_name = self.prompt("Please enter client's full name:")
        email = self.prompt("Please enter client's email:")
        phone_number = self.prompt("Please enter client's phone number:")
        decision = self.prompt_choice(
            "Does client belong to a company? (Y/N)",
            {"Y", "N"}
            )
        if decision == "Y":
            company = self.prompt("Please enter company name:")
        else:
            company = None
        return full_name, email, phone_number, company

    def get_client_name(self):
        """
        Prompt the user to enter the name of a client to modify.

        Returns:
            str: The client's full name as entered by the user.
        """
        return self.prompt(("Enter the name of the client "
                            "to modify as listed above"))

    def get_modif_client_info(self):
        """
        Prompt the user to enter updated information for an existing client.

        Returns:
            tuple: A tuple containing updated client data:
                (full_name, email, phone_number, company_name).
        """
        self.message('Enter new client information:')
        name, email, phone_number, comp = self.get_info_client()
        return name, email, phone_number, comp
