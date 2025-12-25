from db_connector import get_db_connection
import bcrypt


class User:

    def __init__(self, email, name, password_hash, id=None):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.unique_id = id

    def save_user_to_db(self):
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO user (name, email, password_hush)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (self.name, self.email, self.password_hash))
        connection.commit()

        cursor.close()
        connection.close()
        return None


def find_user(email, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """SELECT email, password_hush FROM user WHERE email = %s"""
    cursor.execute(query, (email,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    stored_hash = results[0][1].encode()
    pass_match = bcrypt.checkpw(password.encode(), stored_hash)
    if pass_match:
        """Generate token here"""
        return True
    else:
        return False
