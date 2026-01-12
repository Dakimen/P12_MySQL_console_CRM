import bcrypt


class CollaboratorController:
    def __init__(self, auth_service, collab_view, collab_service, sentry):
        self.auth_service = auth_service
        self.collab_view = collab_view
        self.collab_service = collab_service
        self.sentry = sentry

    def change_password(self):
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
        results = self.collab_service.get_all()
        for result in results:
            self.collab_view.display_collab(result)

    def add_collab(self):
        created_by = self.auth_service.get_user_id()
        name, email, temp_hush = self.collab_view.get_new_collab_info()
        self.collab_service.save_user_to_db(name, email, temp_hush)
        self.sentry.create_collaborator(name, email, created_by)
        return self.collab_view.message("Collaborator added!")

    def modif_name(self):
        updated_by = self.auth_service.get_user_id()
        email, name = self.collab_view.modif_name_view()
        self.collab_service.update_user_name(name, email)
        self.sentry.update_collaborator_name(name, email, updated_by)
        return self.collab_view.message("Collaborator modified")

    def modif_email(self):
        updated_by = self.auth_service.get_user_id()
        name, email = self.collab_view.modif_email_view()
        self.collab_service.update_user_email(email, name)
        self.sentry.update_collaborator_email(name, email, updated_by)
        return self.collab_view.message("Collaborator modified")

    def assign_role(self):
        updated_by = self.auth_service.get_user_id()
        email = self.collab_view.get_email()
        role_choice = self.collab_view.get_role()
        self.collab_service.assign_role(email, role_choice)
        self.sentry.update_collaborator_role(self, email,
                                             role_choice, updated_by)
        return self.collab_view.message("Role assigned")

    def find_user_by_email(self, email, password):
        results = self.collab_service.find_user_by_email(email)
        if not results:
            return None, None
        user_id, stored_hush, _ = results[0]
        if not self.auth_service.check_password(password, stored_hush):
            return None, None
        role_titles = [row[2] for row in results]
        return user_id, role_titles
