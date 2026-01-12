class ClientController:
    """
    Handles client-related actions.

    Client Controller is responsible for handling client-related commands,
    such as displaying, searching, adding and modifying clients.
    """
    def __init__(self, client_view, client_service, auth_service):
        """
            Initialize the client controller.

            Stores references to required client view, client service and
            authentication service.

            Args:
            client_view: View responsible for client-related actions.
            client_service: Service handling client-related actions.
            auth_service: Service responsible for authentication.
        """
        self.client_view = client_view
        self.client_service = client_service
        self.auth_service = auth_service

    def display_all_clients(self):
        """
        Recuperate all clients and display them with the help of client view
        """
        clients = self.client_service.get_all_clients()
        for client in clients:
            self.client_view.display_client(client)

    def find_client_name(self):
        """
        Find client by their name.

        Displays client information on success,
        prints "Client not found" otherwise.
        """
        name = self.client_view.get_client_search_key("full name")
        clients = self.client_service.find_by_name(name)
        if clients is not None:
            for client in clients:
                self.client_view.display_client(client)
        else:
            self.client_view.message("Client not found")

    def find_client_email(self):
        """
        Find client by their email.

        Displays client information on success,
        prints "Client not found" otherwise.
        """
        email = self.client_view.get_client_search_key("email")
        clients = self.client_service.find_by_email(email)
        if clients is not None:
            for client in clients:
                self.client_view.display_client(client)
        else:
            self.client_view.message("Client not found")

    def add_client(self):
        """
        Manages client addition.

        Recuperates new client information and calls on client service
        to add the new client to the database
        """
        full_name, email, phone, company = self.client_view.get_info_client()
        user_id = self.auth_service.get_user_id()

        self.client_service.create_client(
            full_name, email, phone, company, user_id
        )
        self.client_view.message("Client added successfully!")

    def display_own_clients(self):
        """
        Recuperate and display clients of the current user.
        """
        user_id = self.auth_service.get_user_id()
        clients = self.client_service.get_clients_for_user(user_id)
        for client in clients:
            self.client_view.display_client(client)

    def update(self):
        """
        Manage client information update.

        Collects updated client information and passes it to client service.
        """
        user_id = self.auth_service.get_user_id()
        self.display_own_clients()

        old_name = self.client_view.get_client_name()
        new_data = self.client_view.get_modif_client_info()

        self.client_service.update_client(old_name, new_data, user_id)
        self.client_view.message(
            ("Client updated successfully!"
             "Please verify that information "
             "was added correctly through client search")
             )
