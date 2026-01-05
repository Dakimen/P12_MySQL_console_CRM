from datetime import datetime


class ClientView:
    def __init__(self):
        pass

    def display_clients(self, result):
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
