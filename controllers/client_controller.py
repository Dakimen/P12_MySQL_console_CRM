from datetime import datetime

from data_manager.db_choice import data_manager
from controllers.auth_controller import AuthService


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

    def find_client_name(self):
        name = self.client_view.get_client_search_key("full name")
        query = """SELECT
                full_name, email, phone_number
                company_name, date_created, last_updated
                FROM client
                WHERE client.full_name = %s"""
        results = data_manager.make_query(query, (name,))
        for result in results:
            self.client_view.display_clients(result)

    def find_client_email(self):
        email = self.client_view.get_client_search_key("email")
        query = """SELECT
                full_name, email, phone_number
                company_name, date_created, last_updated
                FROM client
                WHERE client.email = %s"""
        results = data_manager.make_query(query, (email,))
        for result in results:
            self.client_view.display_clients(result)

    def add_client(self):
        full_name, email, phone_num, comp = self.client_view.get_info_client()
        user_id = AuthService.get_user_id()
        if user_id:
            query = """
            INSERT INTO client
            (full_name, email, phone_number, company_name, commercial_responsible_id)
            VALUES (%s, %s, %s, %s, UUID_TO_BIN(%s))
            """
            data_manager.make_query(query, (full_name, email,
                                            phone_num, comp, user_id,))
            self.client_view.client_added_confirmation()
            return None

    def display_own_clients(self, user_id):
        query = """
        SELECT
        full_name, email, phone_number,
        company_name, date_created, last_updated FROM client
        WHERE commercial_responsible_id = UUID_TO_BIN(%s)
        """
        results = data_manager.make_query(query, (user_id,))
        for result in results:
            self.client_view.display_clients(result)

    def update(self):
        user_id = AuthService.get_user_id()
        self.display_own_clients(user_id)
        client_to_change = self.client_view.get_client_name()
        name, email, phone_num, comp = self.client_view.get_modif_client_info()
        time_update = datetime.now()
        query = """
        UPDATE client
        SET
        full_name = %s,
        email = %s,
        phone_number = %s,
        company_name = %s,
        last_updated = %s
        WHERE commercial_responsible_id = UUID_TO_BIN(%s)
        AND full_name = %s
        """
        data_manager.make_query(query, (name, email,
                                        phone_num, comp,
                                        time_update, user_id,
                                        client_to_change,))
        self.client_view.client_updated_confirmation()
        return None
