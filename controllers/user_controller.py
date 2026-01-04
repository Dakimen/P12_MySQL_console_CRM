from models.user_model import User
from views.user_view import UserView
from data_manager.db_connector import make_query
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

    @classmethod
    def find_user_by_email(cls, email, password):
        query = """
            SELECT
                BIN_TO_UUID(user.id),
                user.password_hush,
                role.title
            FROM user
            JOIN user_role_assignment
                ON user_role_assignment.user_id = user.id
            JOIN role
                ON user_role_assignment.role_id = role.id
            WHERE user.email = %s
        """
        results = make_query(query, (email,))
        if not results:
            return None, None
        user_id, stored_hush, _ = results[0]
        if not AuthService.check_password(password, stored_hush):
            return None, None
        role_titles = [row[2] for row in results]
        return user_id, role_titles

    @classmethod
    def find_user_by_id(cls, user_id):
        query = """SELECT email, name, password_hush
                FROM user
                WHERE id = UUID_TO_BIN(%s)"""
        results = make_query(query, (user_id,))
        email, name, stored_hush = results[0]
        return email, name, stored_hush
