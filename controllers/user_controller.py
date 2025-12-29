from models.user_model import User, find_user
from views.user_view import UserView


class UserController:

    def __init__(self):
        self.view = UserView

    def user_creation_controller(self):
        email, name, pass_hush = self.view.add_user_view()
        user = User(email, name, pass_hush)
        user.save_user_to_db()
        self.view.account_created_info()

    def login_controller(self):
        email, password = self.view.login_view()
        token, name, password_hush = find_user(email, password)
        if token is False:
            self.view.connection_failure()
        else:
            user_account = User(email, name, password_hush, token=token)
            self.view.connection_success()
            return user_account
