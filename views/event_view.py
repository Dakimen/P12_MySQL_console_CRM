from datetime import datetime

from views.base_view import BaseView


class EventView(BaseView):
    def display_event(self, event):
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

    def get_datetime(self):
        while True:
            print(("Please follow the date format: "
                   "dd/mm/yyyy HH:MM (ex: 08/01/2026 19:47)"))
            value = input(">>> ")
            try:
                return datetime.strptime(value, "%d/%m/%Y %H:%M")
            except ValueError:
                print("Invalid date or format.")

    def get_start_and_end(self):
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
        client_name = self.prompt("Please enter the client's full name")
        client_email = self.prompt("Please enter the client's email")
        return client_name, client_email

    def get_new_responsible_email(self):
        return self.prompt("Please enter the new support responsible's email:")

    def get_event_data(self):
        start, end = self.get_start_and_end()
        location = self.prompt("Please enter the event's location:")
        attendees = self.prompt_int('Please enter the number of attendees:')
        notes = self.prompt("Please enter any notes on this event (optional):")
        data = (start, end, location, attendees, notes)
        return data
