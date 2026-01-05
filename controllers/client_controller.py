from data_manager.db_choice import data_manager


class ClientController:
    def __init__(self, client_view):
        self.client_view = client_view

    def display_all_clients(self):
        query = """SELECT
                full_name, email, phone_number
                company_name, date_created, last_updated
                FROM client"""
        results = data_manager.make_query(query, ())
        for result in results:
            self.client_view.display_clients(result)
