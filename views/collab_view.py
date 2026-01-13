from views.base_view import BaseView


class CollaboratorView(BaseView):
    """
    Collaborator view class used for displaying collaborator information
    and collecting collaborator-related user input.

    Inherits from BaseView and relies on its helper methods for
    prompting, messaging, and formatted output.
    """
    def get_pass_input(self):
        """
        Prompts user to enter their current password.

        Returns:
            (str) containing an unhushed password as entered by the user.
        """
        return self.prompt_password("Please enter your current password:")

    def get_new_pass(self):
        """
        Prompts user to enter their new password.

        Returns:
            (str) containing an unhushed password as entered by the user.
        """
        return self.prompt_password("Enter new password:")

    def display_collab(self, result):
        """
        Display a collaborator's information in a formatted section.

        Args:
            result (tuple | list): Collaborator data containing:
                (name, email, role).

        Side Effects:
            - Outputs formatted collaborator information to the user interface.
        """
        self.section()
        self.labeled("Name", result[0])
        self.labeled("Email", result[1])
        self.labeled("Role", result[2])
        self.end_section()

    def get_new_collab_info(self):
        """
        Prompts user to enter new collaborator's informations.

        Returns:
            name (str): New collaborator's name.
            email (str): New collaborator's email.
            password (str): Yet unhushed new collaborator's temporary password.
        """
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
        """
        Prompts user to enter values needed for collaborator's name update.

        Returns:
            email (str): Email of the collaborator to modify.
            name (str): Collaborator's new name.
        """
        email = self.prompt("Enter the email of collaborator to modify:")
        name = self.prompt("Enter collaborator's new name:")
        return email, name

    def modif_email_view(self):
        """
        Prompts user to enter values needed for collaborator's email update.

        Returns:
            name (str): Name of the collaborator to modify.
            email (str): Collaborator's new email.
        """
        name = self.prompt("Enter the name of collaborator to modify:")
        email = self.prompt("Enter collaborator's new email:")
        return name, email

    def get_email(self):
        """
        Prompts user to enter a collaborator's email.

        Returns:
            email (str): Email as entered by user.
        """
        return self.prompt("Enter collaborator's email:")

    def get_role(self):
        """
        Prompts user to choose a role from a list.

        List contains:
            "commercial responsible"
            "management responsible"
            "support responsible"

        Returns:
            role (str): Chosen role.
        """
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
        """
        Prompts user to enter login informations.

        Returns:
            email (str): Entered email.
            password (str): Entered password.
        """
        self.message("Login.")
        email = self.prompt("Please enter your email:")
        password = self.prompt_password("Enter your password:")
        return email, password
