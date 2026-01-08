class EventController:
    def __init__(self, event_view, auth_service,
                 event_service, contract_service):
        self.event_view = event_view
        self.auth_service = auth_service
        self.event_service = event_service
        self.contract_service = contract_service

    def display_all(self):
        results = self.event_service.get_all()
        for result in results:
            self.event_view.display_event(result)

    def create_event(self):
        user_id = self.auth_service.get_user_id()
        data = self.event_view.get_event_data()
        start, end, location, attendees, notes, c_name, c_email = data
        contract_id = self.contract_service.get_contract_for_event(c_name,
                                                                   c_email,
                                                                   user_id)
        if contract_id:
            self.event_service.create_event(start, end, location, attendees,
                                            notes, contract_id[0][0])
            self.event_view.added_successfully()
        else:
            self.event_view.contract_not_found()
            return None
