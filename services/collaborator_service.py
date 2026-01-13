from services.base_service import BaseService


class CollaboratorService(BaseService):
    """
    Service class responsible for collaborator-related database operations.

    Inherits from BaseService and relies on its database helper methods.
    """
    def get_pass_hush(self, user_id):
        """
        Find user's password hush by their id.

        Args:
            user_id (str): The user's UUID.

        Returns:
            password_hush (str): The user's hushed password
        """
        query = """
        SELECT password_hush
        FROM user
        WHERE id = UUID_TO_BIN(%s)
        """
        return self._fetch_one_value(query, (user_id,))

    def set_new_pass(self, user_id, new_hush):
        """
        Update user's password hush by finding them via their id.

        Args:
            user_id (str): The user's UUID.
            new_hush (str): The user's new hushed password.

        Returns:
            None
        """
        query = """
        UPDATE user
        SET password_hush = %s
        WHERE user.id = UUID_TO_BIN(%s)
        """
        return self._execute(query, (new_hush, user_id))

    def get_all(self):
        """
        Retrieve all collaborators from the database.

        Returns:
            list[tuple]: A list of collaborator records, each containing:
            (name(str), email(str), role(str)).
        """
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
        return self._fetch_all(query, ())

    def save_user_to_db(self, name, email, hush):
        """
        Create a new user record in the database.

        Args:
            name (str): User's name.
            email (str): User's email address.
            hush (str): User's temporary password, hushed.

        Returns:
            None

        Side Effects:
            - Inserts a new row into the `user` table.
        """
        query = """
        INSERT INTO user (name, email, password_hush)
        VALUES (%s, %s, %s)
        """
        return self._execute(query, (name, email, hush))

    def update_user_name(self, name, email):
        """
        Update an existing user's name.

        The user is identified by their current email.

        Args:
            name (str): The user's new name.
            email (str): email used to identify which user to update.

        Returns:
            None

        Side Effects:
            - Updates the matching user record in the database.
        """
        query = """
        UPDATE user
        SET name = %s
        WHERE email = %s
        """
        return self._execute(query, (name, email))

    def update_user_email(self, email, name):
        """
        Update an existing user's email.

        The user is identified by their current name.

        Args:
            email (str): The new email to use.
            name (str): The user's name used to identify which user to update.

        Returns:
            None

        Side Effects:
            - Updates the matching user record in the database.
        """
        query = """
        UPDATE user
        SET email = %s
        WHERE name = %s
        """
        return self._execute(query, (email, name))

    def assign_role(self, email, role_choice):
        """
        Assign a role to the specified user

        The user is identified by their current email.

        Args:
            email (str): The email used to identify which user to update.
            role_choice(str): The role as it is named in the database recovered
            from the appropriate view.

        Returns:
            None

        Side Effects:
            - Creates a new user_role_assignment record in the database.
        """
        query = """
        INSERT INTO user_role_assignment (user_id, role_id)
        SELECT user.id, role.id
        FROM user
        JOIN role
        WHERE user.email = %s
        AND role.title = %s
        """
        return self._execute(query, (email, role_choice))

    def find_user_by_email(self, email):
        """
        Find a specific user in the database.

        The user is identified by their current email.

        Args:
            email (str): The email used to identify user.

        Returns:
            list[tuple]: A list of user_role_assignment records,
            each containing:
            (user_id(str), user_password_hush(str), role_title).
            This allows to recover multiple roles if user has more than one.
        """
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
        return self._fetch_all(query, (email,))
