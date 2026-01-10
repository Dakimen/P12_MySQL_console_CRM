from services.base_service import BaseService


class ContractService(BaseService):
    def create_contract(self, total, remaining, created,
                        signed, com_id, cli_id):
        query = """
        INSERT INTO contract
        (amount_total, amount_remaining, created_at, signed,
        commercial_responsible_id, client_id)
        VALUES (%s, %s, %s, %s, UUID_TO_BIN(%s), UUID_TO_BIN(%s))
        """
        self._execute(
            query,
            (total, remaining, created, signed, com_id, cli_id)
        )

    def get_all(self):
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
        return self._fetch_one(query, (name, email, resp_id, signed))

    def get_contract_event_upd(self, name, email, created):
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
        return self._fetch_one(query, (name, email, created))

    def update_contract(self, full, remaining, created, signed, client, resp):
        query = """
        UPDATE contract
        SET
            amount_total = %s,
            amount_remaining = %s,
            signed = %s
        WHERE commercial_responsible_id = UUID_TO_BIN(%s)
          AND client_id = UUID_TO_BIN(%s)
          AND created_at = %s
        """
        return self._execute(query, (full, remaining,
                                     signed, resp, client, created))

    def filter_by_not_signed(self, user_id):
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
