import bcrypt


class CollaboratorController:
    """
    Handles collaborator-related actions.

    Collaborator Controller is responsible for handling
    collaborator-related commands,
    such as displaying, searching, adding and modifying collaborators,
    as well as permitting logged in collaborators to change their password.
    """
    def __init__(self, auth_service, collab_view, collab_service, sentry):
        """
            Initialize the collaborator controller.

            Stores references to required authentication service,
            collaborator view, collaborator service and sentry.

            Args:
            auth_service: Service responsible for authentication.
            collab_view: View responsible for collaborator-related actions.
            collab_service: Service handling collaborator-related actions.
            sentry: Service handling Sentry journalisation.
        """
        self.auth_service = auth_service
        self.collab_view = collab_view
        self.collab_service = collab_service
        self.sentry = sentry

    def change_password(self):
        """
        Manages password change procedure

        Prompts user to enter their password and allows them
        to type a new one on successful validation.
        Prints out an error message otherwise.
        """
        user_id = self.auth_service.get_user_id()
        hush = self.collab_service.get_pass_hush(user_id)
        user_pass_input = self.collab_view.get_pass_input()
        if bcrypt.checkpw(user_pass_input.encode(), hush.encode()):
            new_pass = self.collab_view.get_new_pass()
            new_hush = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())
            self.collab_service.set_new_pass(user_id, new_hush)
            self.collab_view.message("Password changed successfully!")
            return self.auth_service.clean_json_temp('temp.json')
        else:
            return self.collab_view.message(
                "Password change failed, incorrect password"
                )

    def get_all(self):
        """
        Prints out all current collaborators' names and emails.
        """
        results = self.collab_service.get_all()
        try:
            for result in results:
                self.collab_view.display_collab(result)
        except TypeError:
            self.collab_view.message("Nothing found!")

    def add_collab(self):
        """
        Manages collaborator addition.

        Gathers new collaborator information
        and passes it to the collaborator service.
        Sends a sentry notification on successful addition.
        """
        created_by = self.auth_service.get_user_id()
        name, email, temp_hush = self.collab_view.get_new_collab_info()
        temp_hush = bcrypt.hashpw(temp_hush.encode(), bcrypt.gensalt())
        self.collab_service.save_user_to_db(name, email, temp_hush)
        self.sentry.create_collaborator(name, email, created_by)
        return self.collab_view.message("Collaborator added!")

    def modif_name(self):
        """
        Manages collaborator name modification.
        """
        updated_by = self.auth_service.get_user_id()
        email, name = self.collab_view.modif_name_view()
        self.collab_service.update_user_name(name, email)
        self.sentry.update_collaborator_name(name, email, updated_by)
        return self.collab_view.message("Collaborator modified")

    def modif_email(self):
        """
        Manages collaborator email modification.
        """
        updated_by = self.auth_service.get_user_id()
        name, email = self.collab_view.modif_email_view()
        self.collab_service.update_user_email(email, name)
        self.sentry.update_collaborator_email(name, email, updated_by)
        return self.collab_view.message("Collaborator modified")

    def assign_role(self):
        """
        Handles role assignation to a given collaborator.
        """
        updated_by = self.auth_service.get_user_id()
        email = self.collab_view.get_email()
        role_choice = self.collab_view.get_role()
        self.collab_service.assign_role(email, role_choice)
        self.sentry.update_collaborator_role(email,
                                             role_choice, updated_by)
        return self.collab_view.message("Role assigned")

    def find_user_by_email(self, email, password):
        """
        Manages user search by email. Used for login.

        :param email: string containing user's email
        :param password: Unhushed password for validation.
        """
        results = self.collab_service.find_user_by_email(email)
        if not results:
            return None, None
        user_id, stored_hush, _ = results[0]
        if not self.auth_service.check_password(password, stored_hush):
            return None, None
        role_titles = [row[2] for row in results]
        return user_id, role_titles
