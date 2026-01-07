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
