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
        print(f"Date created: {datetime.strftime(result[3],
                                                 "%d/%m/%Y, %H:%M:%S")}")
        if not result[4] is None:
            print(f"Last updated: {datetime.strftime(result[4],
                                                     "%d/%m/%Y, %H:%M:%S")}")
        print("====================")

    @staticmethod
    def get_client_search_key(keyword):
        print(f"Please enter client's {keyword}")
        user_input = input(">>> ")
        return user_input

    @staticmethod
    def get_info_client():
        print("Client addition:")
        print("Please enter client's full name:")
        full_name = input(">>> ")
        print("Please enter client's email:")
        email = input(">>> ")
        print("Please enter client's phone number:")
        phone_number = input(">>> ")
        return full_name, email, phone_number

    @staticmethod
    def client_added_confirmation():
        print("Client added successfully!")
