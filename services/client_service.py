from datetime import datetime

from services.base_service import BaseService


class ClientService(BaseService):
    def get_all_clients(self):
        query = """
        SELECT
            full_name, email, phone_number,
            company_name, date_created, last_updated
        FROM client
        """
        return self._fetch_all(query, ())

    def find_by_name(self, name):
        query = """
        SELECT
            full_name, email, phone_number,
            company_name, date_created, last_updated
        FROM client
        WHERE full_name = %s
        """
        return self._fetch_all(query, (name,))

    def find_by_email(self, email):
        query = """
        SELECT
            full_name, email, phone_number,
            company_name, date_created, last_updated
        FROM client
        WHERE email = %s
        """
        return self._fetch_all(query, (email,))

    def create_client(self, full_name, email, phone, company, user_id):
        query = """
        INSERT INTO client
        (full_name, email, phone_number, company_name,
        commercial_responsible_id)
        VALUES (%s, %s, %s, %s, UUID_TO_BIN(%s))
        """
        self._execute(
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
        return self._fetch_all(query, (user_id,))

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
        self._execute(
            query,
            (name, email, phone, company, datetime.now(), user_id, old_name)
        )

    def get_client_with_responsible(self, name, email):
        query = """
        SELECT
        BIN_TO_UUID(id), BIN_TO_UUID(commercial_responsible_id)
        FROM client
        WHERE full_name = %s AND email = %s
        """
        return self._fetch_one(query, (name, email))
