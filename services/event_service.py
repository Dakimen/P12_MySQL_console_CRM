from data_manager.db_choice import data_manager


class EventService:
    def get_all(self):
        query = """
        SELECT
            event.event_start,
            event.event_end,
            event.location,
            event.attendees,
            event.notes,
            client.full_name,
            COALESCE(user.name, 'Unassigned') AS support_name
        FROM event
        JOIN contract
            ON event.contract_id = contract.id
        JOIN client
            ON contract.client_id = client.id
        LEFT JOIN user
            ON event.support_id IS NOT NULL
        AND event.support_id = user.id
        """
        return data_manager.make_query(query, ())

    def create_event(self, start, end, location,
                     attendees, notes, contract_id):
        query = """
        INSERT INTO event
        (event_start, event_end, location, attendees, notes, contract_id)
        VALUES
        (%s, %s, %s, %s, %s, UUID_TO_BIN(%s))
        """
        return data_manager.make_query(query, (start, end, location,
                                               attendees, notes,
                                               contract_id))

    def get_all_own(self, user_id):
        query = """
        SELECT
            event.event_start,
            event.event_end,
            event.location,
            event.attendees,
            event.notes,
            client.full_name,
            user.name
        FROM event
        JOIN contract
            ON event.contract_id = contract.id
        JOIN client
            ON contract.client_id = client.id
        JOIN user
            ON event.support_id = user.id
        WHERE event.support_id = UUID_TO_BIN(%s)
        """
        return data_manager.make_query(query, (user_id,))

    def get_all_no_support(self):
        query = """
        SELECT
            event.event_start,
            event.event_end,
            event.location,
            event.attendees,
            event.notes,
            client.full_name
        FROM event
        JOIN contract
            ON event.contract_id = contract.id
        JOIN client
            ON contract.client_id = client.id
        WHERE event.support_id IS NULL
        """
        return data_manager.make_query(query, ())

    def find_event(self, name, email):
        query = """
        SELECT
            event.event_start,
            event.event_end,
            event.location,
            event.attendees,
            event.notes,
            client.full_name,
            COALESCE(user.name, 'Unassigned') AS support_name
        FROM event
        JOIN contract
            ON event.contract_id = contract.id
        JOIN client
            ON contract.client_id = client.id
        LEFT JOIN user
            ON event.support_id IS NOT NULL
        AND event.support_id = user.id
        WHERE client.full_name = %s
        AND client.email = %s
        """
        return data_manager.make_query(query, (name, email))

    def modify_event(self, start, end, location,
                     attendees, notes, support, contract_id):
        query = """
        UPDATE event
        SET
            event_start = %s,
            event_end   = %s,
            location    = %s,
            attendees   = %s,
            notes       = %s,
            support_id = (
                SELECT id
                FROM `user`
                WHERE email = %s
            )
        WHERE contract_id = UUID_TO_BIN(%s);
        """
        return data_manager.make_query(query, (start, end, location,
                                               attendees, notes, support,
                                               contract_id))
