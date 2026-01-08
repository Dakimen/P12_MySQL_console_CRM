import re
from datetime import datetime


class EventView:
    def __init__(self):
        self.attendee_format = r"^[0-9]+$"

    def client_not_found(self):
        print("Client not found")

    def added_successfully(self):
        print("The event was created successfully!")

    def display_event(self, event):
        print("")
        print("====================")
        print(f"Client: {event[5]}")
        print(f"Dates: {event[0]} - {event[1]}")
        print(f"Location: {event[2]}")
        print(f"Number of attendees: {event[3]}")
        if event[4]:
            print(f"Notes: {event[4]}")
        try:
            print(f"Support: {event[6]}")
        except IndexError:
            print("Support: Unassigned")
        print("====================")

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
        print("Please enter the event's start date:")
        start = self.get_datetime()
        while True:
            print("Please enter the event's end date:")
            end = self.get_datetime()
            if end < start:
                print("Event's end must be after it's start")
                continue
            return start, end

    def get_attendees(self):
        print('Please enter the number of attendees:')
        while True:
            print("Only enter numbers, ex: 30")
            attendees = input(">>> ")
            if not re.match(self.attendee_format, attendees):
                continue
            return attendees

    def get_client_data(self):
        print("Please enter the client's full name")
        client_name = input(">>> ")
        print("Please enter the client's email")
        client_email = input(">>> ")
        return client_name, client_email

    def get_new_responsible_email(self):
        print("Please enter the new support responsible's email:")
        email = input(">>> ")
        return email

    def get_event_data(self):
        print("")
        start, end = self.get_start_and_end()
        print("Please enter the event's location:")
        location = input(">>> ")
        attendees = self.get_attendees()
        print("Please enter any notes on this event (optional):")
        notes = input(">>> ")
        data = (start, end, location, attendees, notes)
        return data

    def event_search(self):
        print("Event search")

    def modif_start(self):
        print("Event modification")
        print("Enter the following information to find the event to modify")

    def modif_new(self):
        print("Enter the following informations as new event information")

    def modif_end(self):
        print("Event information modified successfully")
