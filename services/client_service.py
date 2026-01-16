from datetime import datetime

from services.base_service import BaseService


class ClientService(BaseService):
    """
    Service class responsible for client-related database operations.

    Inherits from BaseService and relies on its database helper methods.
    """
    def get_all_clients(self):
        """
        Retrieve all clients from the database.

        Returns:
            list[tuple]: A list of client records, each containing:
            (full_name, email, phone_number, company_name,
             date_created, last_updated).
        """
        query = """
        SELECT
            full_name, email, phone_number,
            company_name, date_created, last_updated
        FROM client
        """
        return self._fetch_all(query, ())

    def find_by_name(self, name):
        """
        Find clients by their full name.

        Args:
            name (str): The client's full name.

        Returns:
            list[tuple]: A list of matching client records.
        """
        query = """
        SELECT
            full_name, email, phone_number,
            company_name, date_created, last_updated
        FROM client
        WHERE full_name = %s
        """
        return self._fetch_all(query, (name,))

    def find_by_email(self, email):
        """
        Find clients by their email address.

        Args:
            email (str): The client's email address.

        Returns:
            list[tuple]: A list of matching client records.
        """
        query = """
        SELECT
            full_name, email, phone_number,
            company_name, date_created, last_updated
        FROM client
        WHERE email = %s
        """
        return self._fetch_all(query, (email,))

    def create_client(self, full_name, email, phone, company, user_id):
        """
        Create a new client record in the database.

        Args:
            full_name (str): Client's full name.
            email (str): Client's email address.
            phone (str): Client's phone number.
            company (str): Client's company name.
            user_id (str): UUID of the commercial responsible user.

        Returns:
            True | False

        Side Effects:
            - Inserts a new row into the `client` table.
        """
        query = """
        INSERT INTO client
        (full_name, email, phone_number, company_name,
        commercial_responsible_id)
        VALUES (%s, %s, %s, %s, UUID_TO_BIN(%s))
        """
        affected = self._execute(
            query,
            (full_name, email, phone, company, user_id)
        )
        return affected > 0

    def get_clients_for_user(self, user_id):
        """
        Retrieve all clients assigned to a specific
        commercial responsible user.

        Args:
            user_id (str): UUID of the commercial responsible user.

        Returns:
            list[tuple]: A list of client records associated with the user.
        """
        query = """
        SELECT
            full_name, email, phone_number,
            company_name, date_created, last_updated
        FROM client
        WHERE commercial_responsible_id = UUID_TO_BIN(%s)
        """
        return self._fetch_all(query, (user_id,))

    def update_client(self, old_name, new_data, user_id):
        """
        Update an existing client's information.

        The client is identified by their current name and the
        commercial responsible user's ID.

        Args:
            old_name (str): The client's current full name.
            new_data (tuple): A tuple containing the updated client data:
                (full_name, email, phone_number, company_name).
            user_id (str): UUID of the commercial responsible user.

        Returns:
            True | False

        Side Effects:
            - Updates the matching client record in the database.
            - Updates the `last_updated` timestamp.
        """
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
        affected = self._execute(
            query,
            (name, email, phone, company, datetime.now(), user_id, old_name)
        )
        return affected > 0

    def get_client_with_responsible(self, name, email):
        """
        Retrieve a client ID along with its commercial responsible ID.

        Args:
            name (str): Client's full name.
            email (str): Client's email address.

        Returns:
            tuple | None: A tuple containing:
                (client_id, commercial_responsible_id) as UUID strings,
                or None if no matching client is found.
        """
        query = """
        SELECT
        BIN_TO_UUID(id), BIN_TO_UUID(commercial_responsible_id)
        FROM client
        WHERE full_name = %s AND email = %s
        """
        return self._fetch_one(query, (name, email))
