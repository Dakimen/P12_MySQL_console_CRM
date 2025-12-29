import bcrypt
from datetime import datetime, timedelta
import jwt

from db_connector import make_query, get_db_connection
from config import JWT_ALGORITHM, JWT_SECRET_KEY


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


def find_user(email, password):
    query = ("""SELECT BIN_TO_UUID(user.id), """
             """BIN_TO_UUID(user_role_assignment.role_id), """
             """user.name, user.password_hush """
             """FROM user_role_assignment """
             """JOIN user """
             """ON user_role_assignment.user_id = user.id """
             """WHERE user.email = %s""")
    results = make_query(query, (email,))
    try:
        stored_hush = results[3].encode()
        pass_match = bcrypt.checkpw(password.encode(), stored_hush)
        name = results[2]
        if pass_match:
            user_id = results[0]
            role_id = results[1]
            token = generate_web_token(user_id, role_id)
            return token, name, stored_hush
        else:
            return False, None, None
    except IndexError:
        return False, None, None


def generate_web_token(user_id, role_id):
    time_now = datetime.now()
    time_exp = time_now + timedelta(hours=2)
    time_now = time_now.strftime("%d.%m.%Y %H:%M:%S")
    time_exp = time_exp.strftime("%d.%m.%Y %H:%M:%S")
    payload_jwt = {'id': user_id, 'role': role_id,
                   'generated': time_now, 'exp': time_exp}
    token = jwt.encode(payload_jwt, JWT_SECRET_KEY, JWT_ALGORITHM)
    return token
