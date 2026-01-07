from datetime import datetime

from data_manager.db_choice import data_manager
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

    def add_contract(self):
        client = self.find_client_for_contract()
        if client:
            client_id, com_id = client[0]
            full, paid, created, signed = self.contract_view.get_contract_details()
            try:
                remaining = int(full) - int(paid)
            except ValueError:
                self.contract_view.something_went_wrong()
                return None
            created = datetime.strptime(created, "%d/%m/%Y")
            if signed:
                signed = datetime.strptime(signed, "%d/%m/%Y")
            self.contract_service.create_contract(full, remaining, created,
                                                  signed, com_id, client_id)
            self.contract_view.contract_created()
            return None

    def show_all(self):
        results = self.contract_service.get_all()
        for result in results:
            self.contract_view.display_contract_info(result)
