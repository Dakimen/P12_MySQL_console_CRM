from views.base_view import BaseView


class CollaboratorView(BaseView):
    def get_pass_input(self):
        return self.prompt_password("Please enter your current password:")

    def get_new_pass(self):
        return self.prompt_password("Enter new password:")

    def display_collab(self, result):
        self.section()
        self.labeled("Name", result[0])
        self.labeled("Email", result[1])
        self.labeled("Role", result[2])
        self.end_section()

    def get_new_collab_info(self):
        self.message("Enter new collaborator's informations:")
        name = self.prompt("Name:")
        email = self.prompt("Email:")
        while True:
            password = self.prompt_password(
                "Temporary password for first login:"
                )
            password2 = self.prompt_password("Again:")
            if password != password2:
                self.message("Passwords don't match, try again.")
                continue
            return name, email, password

    def modif_name_view(self):
        email = self.prompt("Enter the email of collaborator to modify:")
        name = self.prompt("Enter collaborator's new name:")
        return email, name

    def modif_email_view(self):
        name = self.prompt("Enter the name of collaborator to modify:")
        email = self.prompt("Enter collaborator's new email:")
        return name, email

    def get_email(self):
        return self.prompt("Enter collaborator's email:")

    def get_role(self):
        choice = self.prompt_choice(
            "Pick role:\n1. Commercial\n2. Management\n3. Support",
            {"1", "2", "3"}
        )
        return {
            "1": "commercial responsible",
            "2": "management responsible",
            "3": "support responsible"
        }[choice]

    def login_view(self):
        self.message("Login.")
        email = self.prompt("Please enter your email:")
        password = self.prompt_password("Enter your password:")
        return email, password
