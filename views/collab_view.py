import getpass


class CollaboratorView:
    def get_pass_input(self):
        print("Please enter your current password:")
        password = getpass.getpass()
        return password

    def get_new_pass(self):
        print("Enter new password:")
        new_pass = getpass.getpass()
        return new_pass

    def confirm_new_pass(self):
        return print("Password changed successfully!")

    def new_pass_fail(self):
        return print("Password change failed, incorrect password")

    def display_collab(self, result):
        print("")
        print("====================")
        print(f"Name: {result[0]}")
        print(f"Email: {result[1]}")
        print(f"Role: {result[2]}")
        print("====================")

    def get_new_collab_info(self):
        print("Enter new collaborator's informations:")
        print("Name:")
        name = input(">>> ")
        print("Email:")
        email = input(">>> ")
        while True:
            print("Temporary password for first login:")
            password = getpass.getpass()
            print("Again:")
            password2 = getpass.getpass()
            if password != password2:
                print("Password's don't match, try again.")
                continue
            return name, email, password

    def confirm_collab_added(self):
        print("Collaborator added!")

    def modif_name_view(self):
        print("Enter the email of collaborator to modify:")
        email = input(">>> ")
        print("Enter collaborator's new name:")
        name = input(">>> ")
        return email, name

    def modif_email_view(self):
        print("Enter the name of collaborator to modify:")
        name = input(">>> ")
        print("Enter collaborator's new email:")
        email = input(">>> ")
        return name, email

    def information_modified(self):
        return print("Collaborator modified")

    def get_email(self):
        print("Enter collaborator's email:")
        email = input(">>> ")
        return email

    def get_role(self):
        print("Pick role:")
        print("1. Commercial responsible")
        print("2. Management responsible")
        print("3. Support responsible")
        role_choice = ""
        while role_choice != "1" or role_choice != "2" or role_choice != "3":
            print("Please enter one of the numbers next to the options above")
            role_choice = input(">>> ")
        if role_choice == "1":
            role_choice = "commercial responsible"
        elif role_choice == "2":
            role_choice = "management responsible"
        else:
            role_choice = "support responsible"
        return role_choice
