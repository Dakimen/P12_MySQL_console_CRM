import bcrypt


class CollaboratorController:
    def __init__(self, auth_service, collab_view, collab_service):
        self.auth_service = auth_service
        self.collab_view = collab_view
        self.collab_service = collab_service

    def change_password(self):
        user_id = self.auth_service.get_user_id()
        hush = self.collab_service.get_pass_hush(user_id)
        hush = hush[0][0]
        user_pass_input = self.collab_view.get_pass_input()
        if bcrypt.checkpw(user_pass_input.encode(), hush.encode()):
            new_pass = self.collab_view.get_new_pass()
            new_hush = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())
            self.collab_service.set_new_pass(user_id, new_hush)
            self.collab_view.confirm_new_pass()
            return self.auth_service.clean_json_temp('temp.json')
        else:
            return self.collab_view.new_pass_fail()

    def get_all(self):
        results = self.collab_service.get_all()
        for result in results:
            self.collab_view.display_collab(result)

    def add_collab(self):
        name, email, temp_hush = self.collab_view.get_new_collab_info()
        self.collab_service.save_user_to_db(name, email, temp_hush)
        return self.collab_view.confirm_collab_added()

    def modif_name(self):
        email, name = self.collab_view.modif_name_view()
        self.collab_service.update_user_name(name, email)
        return self.collab_view.information_modified()

    def modif_email(self):
        name, email = self.collab_view.modif_email_view()
        self.collab_service.update_user_email(email, name)
        return self.collab_view.information_modified()

    def assign_role(self):
        email = self.collab_view.get_email()
        role_choice = self.collab_view.get_role()
        self.collab_service.assign_role(email, role_choice)
        return self.collab_view.role_assigned()

    def find_user_by_email(self, email, password):
        results = self.collab_service.get_user_by_email(email)
        if not results:
            return None, None
        user_id, stored_hush, _ = results[0]
        if not self.auth_service.check_password(password, stored_hush):
            return None, None
        role_titles = [row[2] for row in results]
        return user_id, role_titles
