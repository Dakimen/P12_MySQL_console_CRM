from data_manager.db_choice import data_manager


class UserController:

    def __init__(self, user_view, auth_service):
        self.view = user_view
        self.auth_service = auth_service

    def find_user_by_email(self, email, password):
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
        results = data_manager.make_query(query, (email,))
        if not results:
            return None, None
        user_id, stored_hush, _ = results[0]
        if not self.auth_service.check_password(password, stored_hush):
            return None, None
        role_titles = [row[2] for row in results]
        return user_id, role_titles

    def find_user_by_id(self, user_id):
        query = """SELECT email, name, password_hush
                FROM user
                WHERE id = UUID_TO_BIN(%s)"""
        results = data_manager.make_query(query, (user_id,))
        email, name, stored_hush = results[0]
        return email, name, stored_hush
