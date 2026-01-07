from data_manager.db_choice import data_manager


class ContractService:
    def create_contract(self, total, remaining, created,
                        signed, com_id, cli_id):
        query = """
        INSERT INTO contract
        (amount_total, amount_remaining, created_at, signed, commercial_responsible_id, client_id)
        VALUES (%s, %s, %s, %s, UUID_TO_BIN(%s), UUID_TO_BIN(%s))
        """
        data_manager.make_query(
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
        return data_manager.make_query(query, ())

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
        WHERE client.id = UUID_TO_BIN(%s) AND client.commercial_responsible_id = UUID_TO_BIN(%s)
        """
        return data_manager.make_query(query, (cli_id, com_id))

    def update_contract(self, full, remaining, created, signed, client, resp):
        query = """
        UPDATE contract
        SET
            amount_total = %s,
            amount_remaining = %s,
            created_at = %s,
            signed = %s
        WHERE commercial_responsible_id = UUID_TO_BIN(%s)
          AND client_id = UUID_TO_BIN(%s)
        """
        return data_manager.make_query(query, (full, remaining, created,
                                               signed, resp, client))

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
        return data_manager.make_query(query, (user_id,))

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
        return data_manager.make_query(query, (user_id,))
