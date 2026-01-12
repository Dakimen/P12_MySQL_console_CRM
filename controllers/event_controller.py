class EventController:
    """
    Handles event-related actions.

    Event Controller is responsible for handling
    event-related commands,
    such as displaying, searching, adding and modifying events.
    """
    def __init__(self, event_view, auth_service,
                 event_service, contract_service,
                 contract_view):
        """
        Initialize the contract controller.

        Stores references to required contract view, client service,
        authentification service, contract service and sentry.

        :param event_view: View responsible for event prompts.
        :param auth_service: Service responsible for authentification.
        :param event_service: Service responsible for events.
        :param contract_service: Service responsible for contract actions.
        :param contract_view: View responsible for contract prompts.
        """
        self.event_view = event_view
        self.auth_service = auth_service
        self.event_service = event_service
        self.contract_service = contract_service
        self.contract_view = contract_view

    def display_all(self):
        """
        Recovers and displays all events.
        """
        results = self.event_service.get_all()
        for result in results:
            self.event_view.display_event(result)

    def create_event(self):
        """
        Manages event creation.
        """
        user_id = self.auth_service.get_user_id()
        data = self.event_view.get_event_data()
        c_name, c_email = self.event_view.get_client_data()
        start, end, location, attendees, notes = data
        signed = self.contract_view.get_signed()
        contract_id = self.contract_service.get_contract_for_event(c_name,
                                                                   c_email,
                                                                   user_id,
                                                                   signed)
        if contract_id:
            self.event_service.create_event(start, end, location, attendees,
                                            notes, contract_id)
            self.event_view.message("The event was created successfully!")
        else:
            self.event_view.message("Contract not found")
            return None

    def filter_own_events(self):
        """
        Recovers all events tied to this user and displays them.
        """
        user_id = self.auth_service.get_user_id()
        results = self.event_service.get_all_own(user_id)
        for result in results:
            self.event_view.display_event(result)

    def filter_no_support(self):
        """
        Filters and displays events with no support responsible attached.
        """
        results = self.event_service.get_all_no_support()
        if results is not None:
            for result in results:
                self.event_view.display_event(result)
        else:
            self.event_view.message("No matching events found")

    def find_event(self):
        """
        Handles event search and displays the results.
        """
        self.event_view.message("Event search")
        name, email = self.event_view.get_client_data()
        results = self.event_service.find_event(name, email)
        self.event_view.display_event(results)

    def modify_event(self):
        """
        Handles event modification.
        """
        self.event_view.message(
            ("Event modification"
             "\n"
             "Enter the following information to find the event to modify"
             )
             )
        c_name, c_email = self.event_view.get_client_data()
        created = self.contract_view.get_date_created()
        contract_id = self.contract_service.get_contract_event_upd(c_name,
                                                                   c_email,
                                                                   created)
        contract_id = contract_id
        self.event_view.message(
            "Enter the following informations as new event information"
            )
        data = self.event_view.get_event_data()
        start, end, location, attendees, notes = data
        resp_email = self.event_view.get_new_responsible_email()
        self.event_service.modify_event(start, end, location,
                                        attendees, notes,
                                        resp_email, contract_id)
        return self.event_view.message(
            "Event information modified successfully"
            )
