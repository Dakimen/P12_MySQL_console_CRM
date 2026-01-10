from datetime import datetime

from views.client_view import ClientView


class ContractController:
    def __init__(self, contract_view, client_service,
                 auth_service, contract_service):
        self.contract_view = contract_view
        self.client_service = client_service
        self.auth_service = auth_service
        self.contract_service = contract_service

    def find_client_for_contract(self):
        client_name, email = self.contract_view.get_client()
        client = self.client_service.get_client_with_responsible(client_name,
                                                                 email)
        if client:
            return client
        else:
            ClientView.client_not_found()
            return None

    def get_cont_values(self):
        full, paid, signed = self.contract_view.get_contract_details()
        try:
            remaining = int(full) - int(paid)
        except ValueError:
            self.contract_view.something_went_wrong()
            return None
        if signed:
            signed = datetime.strptime(signed, "%d/%m/%Y")
        return full, remaining, signed

    def get_contract_info(self):
        client = self.find_client_for_contract()
        if client:
            client_id, com_id = client[0]
            full, remaining, signed = self.get_cont_values()
            created = self.contract_view.get_date_created()
            created = datetime.strptime(created, "%d/%m/%Y")
            return full, remaining, created, signed, com_id, client_id

    def add_contract(self):
        full, rem, created, signed, com, cli = self.get_contract_info()
        self.contract_service.create_contract(full, rem, created,
                                              signed, com, cli)
        self.contract_view.contract_created()
        return None

    def show_all(self):
        results = self.contract_service.get_all()
        for result in results:
            self.contract_view.display_contract_info(result)

    def find_contract(self):
        client_id, com_id = self.find_client_for_contract()[0]
        results = self.contract_service.get_contracts_client(
            client_id, com_id
            )
        for result in results:
            self.contract_view.display_contract_info(result)
        return client_id, com_id

    def modif_contract(self):
        self.contract_view.display_modif()
        client, resp = self.find_contract()
        created = self.contract_view.get_date_created()
        created = datetime.strptime(created, "%d/%m/%Y")
        self.contract_view.display_modif_new()
        full, remaining, signed = self.get_cont_values()
        self.contract_service.update_contract(full, remaining, created,
                                              signed, client, resp)
        self.contract_view.update_success()

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
