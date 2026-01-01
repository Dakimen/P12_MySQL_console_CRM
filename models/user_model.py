from data_manager.db_connector import get_db_connection


class User:

    def __init__(self, email, name, password_hush, id=None, token=None):
        self.name = name
        self.email = email
        self.password_hush = password_hush
        self.unique_id = id
        self.token = token

    def save_user_to_db(self):
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO user (name, email, password_hush)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (self.name, self.email, self.password_hush))
        connection.commit()

        cursor.close()
        connection.close()
        return None
