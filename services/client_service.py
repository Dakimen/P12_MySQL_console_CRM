from datetime import datetime

from data_manager.db_choice import data_manager


class ClientService:
    def get_all_clients(self):
        query = """
        SELECT
            full_name, email, phone_number,
            company_name, date_created, last_updated
        FROM client
        """
        return data_manager.make_query(query, ())

    def find_by_name(self, name):
        query = """
        SELECT
            full_name, email, phone_number,
            company_name, date_created, last_updated
        FROM client
        WHERE full_name = %s
        """
        return data_manager.make_query(query, (name,))

    def find_by_email(self, email):
        query = """
        SELECT
            full_name, email, phone_number,
            company_name, date_created, last_updated
        FROM client
        WHERE email = %s
        """
        return data_manager.make_query(query, (email,))

    def create_client(self, full_name, email, phone, company, user_id):
        query = """
        INSERT INTO client
        (full_name, email, phone_number, company_name, commercial_responsible_id)
        VALUES (%s, %s, %s, %s, UUID_TO_BIN(%s))
        """
        data_manager.make_query(
            query,
            (full_name, email, phone, company, user_id)
        )

    def get_clients_for_user(self, user_id):
        query = """
        SELECT
            full_name, email, phone_number,
            company_name, date_created, last_updated
        FROM client
        WHERE commercial_responsible_id = UUID_TO_BIN(%s)
        """
        return data_manager.make_query(query, (user_id,))

    def update_client(self, old_name, new_data, user_id):
        name, email, phone, company = new_data
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
        data_manager.make_query(
            query,
            (name, email, phone, company, datetime.now(), user_id, old_name)
        )
