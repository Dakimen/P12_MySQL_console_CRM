from services.base_service import BaseService


class ContractService(BaseService):
    """
    Service class responsible for contract-related database operations.

    Inherits from BaseService and relies on its database helper methods.
    """
    def create_contract(self, total, remaining, created,
                        signed, com_id, cli_id):
        """
        Create a new contract record in the database.

        Args:
            total (float | int): Total contract amount.
            remaining (float | int): Remaining amount to be paid.
            created (datetime): Contract creation timestamp.
            signed (bool | None): Contract signature status.
            com_id (str): UUID of the commercial responsible user.
            cli_id (str): UUID of the client.

        Returns:
            None

        Side Effects:
            - Inserts a new row into the `contract` table.
        """
        query = """
        INSERT INTO contract
        (amount_total, amount_remaining, created_at, signed,
        commercial_responsible_id, client_id)
        VALUES (%s, %s, %s, %s, UUID_TO_BIN(%s), UUID_TO_BIN(%s))
        """
        affected = self._execute(
            query,
            (total, remaining, created, signed, com_id, cli_id)
        )
        return affected > 0

    def get_all(self):
        """
        Retrieve all contracts with their associated user and client data.

        Returns:
            list[tuple]: A list of contract records containing:
                (amount_total, amount_remaining, created_at, signed,
                 commercial_responsible_name, client_full_name, client_email).
        """
        query = """
        SELECT contract.amount_total, contract.amount_remaining,
        contract.created_at, contract.signed, user.name, client.full_name,
        client.email
        FROM contract
        JOIN user
        ON contract.commercial_responsible_id = user.id
        JOIN client
        ON contract.client_id = client.id
        """
        return self._fetch_all(query, ())

    def get_contracts_client(self, cli_id, com_id):
        """
        Retrieve all contracts for a specific client
        and commercial responsible.

        Args:
            cli_id (str): UUID of the client.
            com_id (str): UUID of the commercial responsible user.

        Returns:
            list[tuple]: A list of matching contract records.
        """
        query = """
        SELECT contract.amount_total, contract.amount_remaining,
        contract.created_at, contract.signed, user.name, client.full_name,
        client.email
        FROM contract
        JOIN user
        ON contract.commercial_responsible_id = user.id
        JOIN client
        ON contract.client_id = client.id
        WHERE client.id = UUID_TO_BIN(%s)
        AND client.commercial_responsible_id = UUID_TO_BIN(%s)
        """
        return self._fetch_all(query, (cli_id, com_id))

    def get_contract_for_event(self, name, email, resp_id, signed):
        """
        Retrieve a contract ID for event creation or association.

        The contract is identified using client details, commercial
        responsible ID, and signature status.

        Args:
            name (str): Client's full name.
            email (str): Client's email address.
            resp_id (str): UUID of the commercial responsible user.
            signed (bool | None): Contract signature status.

        Returns:
            str | None: Contract UUID as a string if found, otherwise None.
        """
        query = """
        SELECT
            BIN_TO_UUID(contract.id)
        FROM contract
        JOIN client
        ON contract.client_id = client.id
        WHERE client.full_name = %s
        AND client.email = %s
        AND contract.commercial_responsible_id = UUID_TO_BIN(%s)
        AND contract.signed = %s
        """
        return self._fetch_one_value(query, (name, email, resp_id, signed))

    def get_contract_event_upd(self, name, email, created):
        """
        Retrieve a contract ID for event update operations.

        The contract is identified using client details and
        contract creation timestamp.

        Args:
            name (str): Client's full name.
            email (str): Client's email address.
            created (datetime): Contract creation timestamp.

        Returns:
            str | None: Contract UUID as a string if found, otherwise None.
        """
        query = """
        SELECT
            BIN_TO_UUID(contract.id)
        FROM contract
        JOIN client
        ON contract.client_id = client.id
        WHERE client.full_name = %s
        AND client.email = %s
        AND created_at = %s
        """
        return self._fetch_one_value(query, (name, email, created))

    def update_contract(self, full, remaining, created, client, resp):
        """
        Update the financial amounts of an existing contract.

        Args:
            full (float | int): Updated total contract amount.
            remaining (float | int): Updated remaining amount.
            created (datetime): Contract creation timestamp.
            client (str): UUID of the client.
            resp (str): UUID of the commercial responsible user.

        Returns:
            True | False

        Side Effects:
            - Updates the matching contract record in the database.
        """
        query = """
        UPDATE contract
        SET
            amount_total = %s,
            amount_remaining = %s
        WHERE commercial_responsible_id = UUID_TO_BIN(%s)
          AND client_id = UUID_TO_BIN(%s)
          AND created_at = %s
        """
        affected = self._execute(query, (full, remaining,
                                         resp, client, created))
        return affected > 0

    def sign_contract(self, created, client, resp, signed):
        """
        Update the signature status of a contract.

        Args:
            created (datetime): Contract creation timestamp.
            client (str): UUID of the client.
            resp (str): UUID of the commercial responsible user.
            signed (bool): New signature status.

        Returns:
            True | False

        Side Effects:
            - Updates the `signed` field of the contract record.
        """
        query = """
        UPDATE contract
        SET
            signed = %s
        WHERE commercial_responsible_id = UUID_TO_BIN(%s)
          AND client_id = UUID_TO_BIN(%s)
          AND created_at = %s
        """
        affected = self._execute(query, (signed, resp, client, created))
        return affected > 0

    def filter_by_not_signed(self, user_id):
        """
        Retrieve all unsigned contracts for a specific commercial responsible.

        Args:
            user_id (str): UUID of the commercial responsible user.

        Returns:
            list[tuple]: A list of unsigned contract records.
        """
        query = """
        SELECT contract.amount_total, contract.amount_remaining,
        contract.created_at, contract.signed, user.name, client.full_name,
        client.email
        FROM contract
        JOIN user
        ON contract.commercial_responsible_id = user.id
        JOIN client
        ON contract.client_id = client.id
        WHERE client.commercial_responsible_id = UUID_TO_BIN(%s)
        AND contract.signed IS NULL
        """
        return self._fetch_all(query, (user_id,))

    def filter_by_not_paid_off(self, user_id):
        """
        Retrieve all contracts that are not fully paid off.

        Args:
            user_id (str): UUID of the commercial responsible user.

        Returns:
            list[tuple]: A list of contracts with a non-zero remaining amount.
        """
        query = """
        SELECT contract.amount_total, contract.amount_remaining,
        contract.created_at, contract.signed, user.name, client.full_name,
        client.email
        FROM contract
        JOIN user
        ON contract.commercial_responsible_id = user.id
        JOIN client
        ON contract.client_id = client.id
        WHERE client.commercial_responsible_id = UUID_TO_BIN(%s)
        AND contract.amount_remaining != 0
        """
        return self._fetch_all(query, (user_id,))
