from services.base_service import BaseService


class EventService(BaseService):
    """
    Service class responsible for event-related database operations.

    Inherits from BaseService and relies on its database helper methods.
    """
    def get_all(self):
        """
        Retrieve all events with their associated user and client data.

        Returns:
            list[tuple]: A list of event records containing:
                (event_start, event_end, location, attendees(int),
                notes, client's name, and support responsible user's name).
        """
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
        return self._fetch_all(query, ())

    def create_event(self, start, end, location,
                     attendees, notes, contract_id):
        """
        Create a new event record in the database.

        Args:
            start (datetime): The date and time of the event's start.
            end (datetime): The date and time of the event's end.
            location (str): String precising event's location.
            attendees (int|str): Number of attendees expected at the event.
            notes (str): Any notes relating to the event.
            contract_id (UUID): The id of the contract tied to this event.

        Returns:
            None

        Side Effects:
            - Inserts a new row into the `event` table.
        """
        query = """
        INSERT INTO event
        (event_start, event_end, location, attendees, notes, contract_id)
        VALUES
        (%s, %s, %s, %s, %s, UUID_TO_BIN(%s))
        """
        affected = self._execute(query, (start, end, location,
                                         attendees, notes,
                                         contract_id))
        return affected > 0

    def get_all_own(self, user_id):
        """
        Retrieve all events user is responsible for.

        Args:
            user_id (UUID): support user's id.

        Returns:
            list[tuple]: A list of event records containing:
                (event_start, event_end, location, attendees(int),
                notes, client's name, and support responsible user's name).
        """
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
        return self._fetch_all(query, (user_id,))

    def get_all_no_support(self):
        """
        Retrieve all events without an assigned support responsible.

        Returns:
            list[tuple]: (event_start, event_end, location, attendees(int),
                          notes, client's name,
                          and support responsible user's name)
                          of unsigned event records.
        """
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
        return self._fetch_all(query, ())

    def find_event(self, name, email):
        """
        Retrieve all events created for a specific client.

        Args:
            name (str): Target client's full name.
            email (str): Target client's email.

        Returns:
            list[tuple]: (event_start, event_end, location, attendees(int),
                          notes, client's name,
                          and support responsible user's name)
        """
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
        return self._fetch_all(query, (name, email))

    def modify_event(self, start, end, location,
                     attendees, notes, support, contract_id):
        """
        Update the details of a specific event.

        Args:
            start (datetime): Updated start of the target event.
            remaining (float | int): Updated end time of the target event.
            location (str): Updated location of the target event.
            attendees (str | int): Updated number of attendees expected.
            notes (str): Updated notes on the event.
            support (UUID): UUID of the support responsible of this event,
            new or old.
            contract_id (UUID): UUID of the contract used to identify the event
            to update.

        Returns:
            None

        Side Effects:
            - Updates the matching event record in the database.
        """
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
        affected = self._execute(query, (start, end, location,
                                         attendees, notes, support,
                                         contract_id))
        return affected > 0
