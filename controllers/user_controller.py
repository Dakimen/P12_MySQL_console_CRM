from models.user_model import User
from views.user_view import UserView
from data_manager.db_connector import make_query
from controllers.auth_controller import generate_web_token
from controllers.auth_controller import AuthService


class UserController:

    def __init__(self):
        self.view = UserView

    def user_creation_controller(self):
        email, name, pass_hush = self.view.add_user_view()
        user = User(email, name, pass_hush)
        user.save_user_to_db()
        self.view.account_created_info()
        return None

    def login_controller(self):
        email, password = self.view.login_view()
        token, name, password_hush = UserController.find_user_by_email(email, password)
        if token is False:
            self.view.connection_failure()
        else:
            user_account = User(email, name, password_hush, token=token)
            roles = AuthService.get_roles_from_token(token=token)
            AuthService.write_token_to_temp(token)
            return user_account, roles
        return None

    @classmethod
    def find_user_by_email(cls, email, password):
        query = """
            SELECT
                BIN_TO_UUID(user.id),
                user.name,
                user.password_hush,
                BIN_TO_UUID(user_role_assignment.role_id)
            FROM user
            JOIN user_role_assignment
                ON user_role_assignment.user_id = user.id
            WHERE user.email = %s
        """
        results = make_query(query, (email,))
        if not results:
            return False, None, None
        user_id, name, stored_hush, _ = results[0]
        if not AuthService.check_password(password, stored_hush):
            return False, None, None
        role_ids = [row[3] for row in results]
        token = generate_web_token(user_id, role_ids)
        return token, name, stored_hush

    @classmethod
    def find_user_by_id(cls, user_id):
        query = """SELECT email, name, password_hush
                FROM user
                WHERE id = UUID_TO_BIN(%s)"""
        results = make_query(query, (user_id,))
        email, name, stored_hush = results[0]
        return email, name, stored_hush
