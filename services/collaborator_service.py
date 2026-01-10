from data_manager.db_choice import data_manager


class CollaboratorService:
    def get_pass_hush(self, user_id):
        query = """
        SELECT password_hush
        FROM user
        WHERE id = UUID_TO_BIN(%s)
        """
        return data_manager.make_query(query, (user_id,))

    def set_new_pass(self, user_id, new_hush):
        query = """
        UPDATE user
        SET password_hush = %s
        WHERE user.id = UUID_TO_BIN(%s)
        """
        return data_manager.make_query(query, (new_hush, user_id))

    def get_all(self):
        query = """
        SELECT
            `user`.name,
            `user`.email,
            COALESCE(role.title, 'Unassigned') AS role_title
        FROM `user`
        LEFT JOIN user_role_assignment
            ON `user`.id = user_role_assignment.user_id
        LEFT JOIN role
            ON user_role_assignment.role_id = role.id;
        """
        return data_manager.make_query(query, ())

    def save_user_to_db(self, name, email, hush):
        query = """
        INSERT INTO user (name, email, password_hush)
        VALUES (%s, %s, %s)
        """
        data_manager.make_query(query, (name, email, hush))
        return None

    def update_user_name(self, name, email):
        query = """
        UPDATE user
        SET name = %s
        WHERE email = %s
        """
        return data_manager.make_query(query, (name, email))

    def update_user_email(self, email, name):
        query = """
        UPDATE user
        SET email = %s
        WHERE name = %s
        """
        return data_manager.make_query(query, (email, name))

    def assign_role(self, email, role_choice):
        query = """
        INSERT INTO user_role_assignment (user_id, role_id)
        SELECT user.id, role.id
        FROM user
        JOIN role
        WHERE user.email = %s
        AND role.title = %s
        """
        return data_manager.make_query(query, (email, role_choice))

    def get_user_by_email(self, email):
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
        return data_manager.make_query(query, (email,))
