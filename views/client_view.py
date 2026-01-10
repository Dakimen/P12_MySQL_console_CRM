from views.base_view import BaseView


class ClientView(BaseView):
    def display_client(self, client):
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
        return self.prompt(f"Please enter client's {keyword}")

    def get_info_client(self):
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
        return self.prompt(("Enter the name of the client "
                            "to modify as listed above"))

    def get_modif_client_info(self):
        self.message('Enter new client information:')
        name, email, phone_number, comp = self.get_info_client()
        return name, email, phone_number, comp
