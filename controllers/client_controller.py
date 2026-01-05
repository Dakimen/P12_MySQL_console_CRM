import sys

from data_manager.db_choice import data_manager
from controllers.auth_controller import AuthService
from views.auth_view import token_expired_notification


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
        full_name, email, phone_num = self.client_view.get_info_client()
        token = AuthService.get_token_from_temp()
        permission = AuthService.is_jwt_valid(token)
        if permission is True:
            user_id = AuthService.get_user_id_from_token(token)
            query = """
            INSERT INTO client
            (full_name, email, phone_number, commercial_responsible_id)
            VALUES (%s, %s, %s, UUID_TO_BIN(%s))
            """
            data_manager.make_query(query, (full_name, email,
                                            phone_num, user_id,))
            self.client_view.client_added_confirmation()
            return None
        else:
            token_expired_notification()
            sys.exit()
