from data_manager.db_choice import data_manager


class ContractController:
    def __init__(self, contract_view, client_service, auth_service):
        self.contract_view = contract_view
        self.client_service = client_service
        self.auth_service = auth_service
