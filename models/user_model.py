from data_manager.db_choice import data_manager


class User:

    def __init__(self, email, name, password_hush, id=None, token=None):
        self.name = name
        self.email = email
        self.password_hush = password_hush
        self.unique_id = id
        self.token = token

    def save_user_to_db(self):
        query = """
        INSERT INTO user (name, email, password_hush)
        VALUES (%s, %s, %s)
        """
        data_manager.make_query(query, (self.name,
                                        self.email,
                                        self.password_hush))
        return None
