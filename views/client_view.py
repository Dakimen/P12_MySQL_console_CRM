from datetime import datetime


class ClientView:
    def __init__(self):
        pass

    @staticmethod
    def display_clients(result):
        print("\n")
        print("====================")
        print(f"Name: {result[0]}")
        print(f"Email: {result[1]}")
        print(f"Phone number: {result[2]}")
        if result[3] is not None:
            print(f"Company name: {result[3]}")
        print(f"Date created: {datetime.strftime(result[4],
                                                 "%d/%m/%Y, %H:%M:%S")}")
        if not result[5] is None:
            print(f"Last updated: {datetime.strftime(result[5],
                                                     "%d/%m/%Y, %H:%M:%S")}")
        print("====================")

    @staticmethod
    def get_client_search_key(keyword):
        print(f"Please enter client's {keyword}")
        user_input = input(">>> ")
        return user_input

    @staticmethod
    def get_info_client():
        print("Please enter client's full name:")
        full_name = input(">>> ")
        print("Please enter client's email:")
        email = input(">>> ")
        print("Please enter client's phone number:")
        phone_number = input(">>> ")
        decision = None
        while decision != "Y" and decision != 'N':
            print("Does client belong to a company? Y/N")
            decision = input(">>> ").upper()
        if decision == "Y":
            print("Please enter company name:")
            company_name = input(">>> ")
        else:
            company_name = None
        return full_name, email, phone_number, company_name

    @staticmethod
    def client_added_confirmation():
        print("Client added successfully!")

    @staticmethod
    def get_client_name():
        print(("Enter the name of the client "
               "to modify as listed above"))
        client_name = input(">>> ")
        return client_name

    @staticmethod
    def get_modif_client_info():
        print('Enter new client information:')
        name, email, phone_number, comp = ClientView.get_info_client()
        return name, email, phone_number, comp

    @staticmethod
    def client_updated_confirmation():
        print("Client updated successfully!")
        print(("Please verify that information "
               "was added correctly through client search"))
