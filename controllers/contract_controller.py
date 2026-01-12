class ContractController:
    def __init__(self, contract_view, client_service,
                 auth_service, contract_service, sentry):
        self.contract_view = contract_view
        self.client_service = client_service
        self.auth_service = auth_service
        self.contract_service = contract_service
        self.sentry = sentry

    def find_client_for_contract(self):
        client_name, email = self.contract_view.get_client()
        client = self.client_service.get_client_with_responsible(client_name,
                                                                 email)
        if client:
            return client
        else:
            self.contract_view.message("Client not found!")
            return None

    def get_cont_values(self):
        full, paid = self.contract_view.get_contract_details()
        remaining = int(full) - int(paid)
        return full, remaining

    def get_contract_info(self):
        client = self.find_client_for_contract()
        if client:
            client_id, com_id = client
            full, remaining = self.get_cont_values()
            created, signed = self.contract_view.get_created_signed()
            return full, remaining, created, signed, com_id, client_id

    def add_contract(self):
        full, rem, created, signed, com, cli = self.get_contract_info()
        self.contract_service.create_contract(full, rem, created,
                                              signed, com, cli)
        self.contract_view.message("Contract added successfully!")
        return None

    def show_all(self):
        results = self.contract_service.get_all()
        for result in results:
            self.contract_view.display_contract_info(result)

    def find_contract(self):
        client_id, com_id = self.find_client_for_contract()
        results = self.contract_service.get_contracts_client(
            client_id, com_id
            )
        for result in results:
            self.contract_view.display_contract_info(result)
        return client_id, com_id

    def contract_modif_finalize(self, client, resp):
        created = self.contract_view.get_date_created()
        self.contract_view.message(
            "Please enter the contract's new informations:"
            )
        full, remaining = self.get_cont_values()
        self.contract_service.update_contract(full, remaining, created,
                                              client, resp)
        self.contract_view.message("Contract updated successfully!")

    def modif_contract_management(self):
        self.contract_view.message(
            "Please enter the values of the contract to modify:"
            )
        client, resp = self.find_contract()
        return self.contract_modif_finalize(client, resp)

    def filter_not_signed(self):
        user_id = self.auth_service.get_user_id()
        results = self.contract_service.filter_by_not_signed(user_id)
        for result in results:
            self.contract_view.display_contract_info(result)

    def filter_not_paid(self):
        user_id = self.auth_service.get_user_id()
        results = self.contract_service.filter_by_not_paid_off(user_id)
        for result in results:
            self.contract_view.display_contract_info(result)

    def sign_contract(self):
        token = self.auth_service.get_token_from_temp()
        roles = self.auth_service.get_roles(token)
        modif_by = self.auth_service.get_user_id_from_token(token)
        self.contract_view.message(
            "Please enter the values of the contract to modify:"
            )
        client, resp = self.find_contract()
        if modif_by == resp or "management responsible" in roles:
            created = self.contract_view.get_date_created()
            self.contract_view.message(
                "Please enter contract signature details"
                )
            signed = self.contract_view.get_signed()
            if signed is not None:
                self.contract_service.sign_contract(created,
                                                    client, resp, signed)
                self.sentry.sign_contract(client, signed, modif_by)
            else:
                return None
        else:
            return self.contract_view.message("Access denied")

    def router_modif(self):
        token = self.auth_service.get_token_from_temp()
        roles = self.auth_service.get_roles(token)
        if "management responsible" in roles:
            return self.modif_contract_management()
        elif "commercial responsible" in roles:
            return self.modif_contract_own()
        else:
            return None

    def modif_contract_own(self):
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
