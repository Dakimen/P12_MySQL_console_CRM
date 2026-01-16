class ContractController:
    """
    Handles contract-related actions.

    Contract Controller is responsible for handling
    contract-related commands,
    such as displaying, searching, adding and modifying contracts.
    """
    def __init__(self, contract_view, client_service,
                 auth_service, contract_service, sentry):
        """
        Initialize the contract controller.

        Stores references to required contract view, client service,
        authentification service, contract service and sentry.

        :param contract_view: View responsible for contract prompts.
        :param client_service: Service responsible for client-related actions.
        :param auth_service: Service responsible for authentification.
        :param contract_service: Service responsible for contract actions.
        :param sentry: Service handling Sentry journalisation.
        """
        self.contract_view = contract_view
        self.client_service = client_service
        self.auth_service = auth_service
        self.contract_service = contract_service
        self.sentry = sentry

    def find_client_for_contract(self):
        """
        Finds client for contract addition.
        Returns tuple of client_id and their responsible's id.
        Returns None otherwise.
        """
        client_name, email = self.contract_view.get_client()
        client = self.client_service.get_client_with_responsible(client_name,
                                                                 email)
        if client:
            return client
        else:
            self.contract_view.message("Client not found!")
            return None, None

    def get_cont_values(self):
        """
        Gets full and remaining values for contract addition.

        Returns:
        full(str) full price of the agreed contract.
        remaining(str) sum remaining until the contract is fully paid off.
        """
        full, paid = self.contract_view.get_contract_details()
        remaining = int(full) - int(paid)
        return full, remaining

    def get_contract_info(self):
        """
        Collects all details necessary for contract creation.

        Returns:
        full(str) full price of the agreed contract.
        remaining(str) sum remaining until the contract is fully paid off.
        created(datetime) date of the contract's creation.
        signed(datetime or None) date contract was signed or None if NA.
        com_id(str) id of the client's commercial responsible
        client_id(str)
        """
        client = self.find_client_for_contract()
        if client:
            client_id, com_id = client
            full, remaining = self.get_cont_values()
            created, signed = self.contract_view.get_created_signed()
            return full, remaining, created, signed, com_id, client_id

    def add_contract(self):
        """
        Manages contract creation.
        """
        full, rem, created, signed, com, cli = self.get_contract_info()
        self.contract_service.create_contract(full, rem, created,
                                              signed, com, cli)
        self.contract_view.message("Contract added successfully!")
        return None

    def show_all(self):
        """
        Displays all the contracts in the database.
        """
        results = self.contract_service.get_all()
        try:
            for result in results:
                self.contract_view.display_contract_info(result)
        except TypeError:
            self.contract_view.message("Nothing found!")

    def find_contract(self):
        """
        Manages contract search.

        Displays contract info and returns client_id
        and their commercial responsible's id.
        """
        client_id, com_id = self.find_client_for_contract()
        if client_id is None:
            return None
        results = self.contract_service.get_contracts_client(
            client_id, com_id
            )
        try:
            for result in results:
                self.contract_view.display_contract_info(result)
            return client_id, com_id
        except TypeError:
            self.contract_view.message("Nothing found!")
            return None, None

    def contract_modif_finalize(self, client, resp):
        """
        Finalizes contract modification
        when the client and responsible are found.

        :param client: client's id
        :param resp: client's commercial responsible's id
        """
        created = self.contract_view.get_date_created()
        self.contract_view.message(
            "Please enter the contract's new informations:"
            )
        full, remaining = self.get_cont_values()
        self.contract_service.update_contract(full, remaining, created,
                                              client, resp)
        self.contract_view.message("Contract updated successfully!")

    def modif_contract_management(self):
        """
        Manages contract modification for management users.
        """
        self.contract_view.message(
            "Please enter the values of the contract to modify:"
            )
        client, resp = self.find_contract()
        if client is None:
            return None
        return self.contract_modif_finalize(client, resp)

    def filter_not_signed(self):
        """
        Recovers and displays unsigned contracts.
        """
        user_id = self.auth_service.get_user_id()
        results = self.contract_service.filter_by_not_signed(user_id)
        try:
            for result in results:
                self.contract_view.display_contract_info(result)
        except TypeError:
            self.contract_view.message("Nothing found!")

    def filter_not_paid(self):
        """
        Recovers and displays contracts that weren't fully paid.
        """
        user_id = self.auth_service.get_user_id()
        results = self.contract_service.filter_by_not_paid_off(user_id)
        try:
            for result in results:
                self.contract_view.display_contract_info(result)
        except TypeError:
            self.contract_view.message("Nothing found!")

    def sign_contract(self):
        """
        Manages contract update relating to it being signed.

        Allows contract signing for users possessing a management role
        as well as the client's commercial responsible.
        """
        token = self.auth_service.get_token_from_temp()
        roles = self.auth_service.get_roles(token)
        modif_by = self.auth_service.get_user_id_from_token(token)
        self.contract_view.message(
            "Please enter the values of the contract to modify:"
            )
        client, resp = self.find_contract()
        if client is None:
            return None
        if modif_by == resp or "management responsible" in roles:
            created = self.contract_view.get_date_created()
            self.contract_view.message(
                "Please enter contract signature details"
                )
            signed = self.contract_view.get_signed()
            if signed is not None:
                self.contract_service.sign_contract(created,
                                                    client,
                                                    resp,
                                                    signed)
                self.sentry.sign_contract(client, signed, modif_by)
            else:
                return None
        else:
            return self.contract_view.message("Access denied")

    def router_modif(self):
        """
        Manages routing to the appropriate modification function
        based on user role.
        """
        token = self.auth_service.get_token_from_temp()
        roles = self.auth_service.get_roles(token)
        if "management responsible" in roles:
            return self.modif_contract_management()
        elif "commercial responsible" in roles:
            return self.modif_contract_own()
        else:
            return None

    def modif_contract_own(self):
        """
        Manages own contract modification.

        Protects from modifying contracts not belonging to user's clients.
        """
        self.contract_view.message(
            "Please enter the values of the contract to modify:"
            )
        user_id = self.auth_service.get_user_id()
        client_name, email = self.contract_view.get_client()
        client_id, resp_id = self.client_service.get_client_with_responsible(
            client_name, email
            )
        if resp_id == user_id:
            return self.contract_modif_finalize(client_id, user_id)
        else:
            self.contract_view.message(
                "You can only modify your own contracts!"
                )
            return None
