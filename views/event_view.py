from views.base_view import BaseView


class EventView(BaseView):
    """
    Event view class used for displaying event information
    and collecting event-related user input.

    Inherits from BaseView and relies on its helper methods for
    prompting, messaging, and formatted output.
    """
    def display_event(self, event):
        """
        Display an event's information in a formatted section.

        Args:
            event (tuple | list): Event data containing:
                (start date, end date, location, number of attendees,
                notes, client and support representative).

        Side Effects:
            - Outputs formatted event information to the user interface.
        """
        self.section()
        self.labeled("Client", event[5])
        dates = f"{event[0]} - {event[1]}"
        self.labeled("Dates", dates)
        self.labeled("Location", event[2])
        self.labeled("Number of attendees", event[3])
        if event[4]:
            self.labeled("Notes", event[4])
        try:
            self.labeled("Support", event[6])
        except IndexError:
            self.labeled("Support", "Unassigned")
        self.end_section()

    def get_start_and_end(self):
        """
        Prompts user to enter event's start and end dates.
        Prompts follow %d/%m/%Y %H:%M format.

        Returns:
            start (datetime): Event's start date and hour.
            end (datetime): Event's end date and hour.
        """
        start = self.prompt_date("Please enter the event's start date:",
                                 "%d/%m/%Y %H:%M")
        while True:
            end = self.prompt_date("Please enter the event's end date:",
                                   "%d/%m/%Y %H:%M")
            if end < start:
                self.message("Event's end must be after it's start")
                continue
            return start, end

    def get_client_data(self):
        """
        Prompts user to enter client's informations for event search.

        Returns:
            client_name (str): Client's full name.
            client_email (str): Client's email.
        """
        client_name = self.prompt("Please enter the client's full name")
        client_email = self.prompt("Please enter the client's email")
        return client_name, client_email

    def get_new_responsible_email(self):
        """
        Prompts user to enter the email of a new support responsible for
        event assignation.

        Returns:
            email (str): Support responsible's email as entered by the user.
        """
        return self.prompt("Please enter the new support responsible's email:")

    def get_event_data(self):
        """
        Prompts user to enter data necessary for event addition.

        Returns:
            data (tuple): event data containing: (start date, end date,
            location, number of attendees, notes)
        """
        start, end = self.get_start_and_end()
        location = self.prompt("Please enter the event's location:")
        attendees = self.prompt_int('Please enter the number of attendees:')
        notes = self.prompt("Please enter any notes on this event (optional):")
        data = (start, end, location, attendees, notes)
        return data
