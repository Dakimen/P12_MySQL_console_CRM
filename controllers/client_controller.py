class ClientController:
    def __init__(self, client_view, client_service, auth_service):
        self.client_view = client_view
        self.client_service = client_service
        self.auth_service = auth_service

    def display_all_clients(self):
        clients = self.client_service.get_all_clients()
        for client in clients:
            self.client_view.display_clients(client)

    def find_client_name(self):
        name = self.client_view.get_client_search_key("full name")
        clients = self.client_service.find_by_name(name)
        for client in clients:
            self.client_view.display_clients(client)

    def find_client_email(self):
        email = self.client_view.get_client_search_key("email")
        clients = self.client_service.find_by_email(email)
        for client in clients:
            self.client_view.display_clients(client)

    def add_client(self):
        full_name, email, phone, company = self.client_view.get_info_client()
        user_id = self.auth_service.get_user_id()

        if not user_id:
            return

        self.client_service.create_client(
            full_name, email, phone, company, user_id
        )
        self.client_view.client_added_confirmation()

    def display_own_clients(self):
        user_id = self.auth_service.get_user_id()
        clients = self.client_service.get_clients_for_user(user_id)
        for client in clients:
            self.client_view.display_clients(client)

    def update(self):
        user_id = self.auth_service.get_user_id()
        self.display_own_clients()

        old_name = self.client_view.get_client_name()
        new_data = self.client_view.get_modif_client_info()

        self.client_service.update_client(old_name, new_data, user_id)
        self.client_view.client_updated_confirmation()
