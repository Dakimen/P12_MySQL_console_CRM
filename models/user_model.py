import bcrypt
import jwt
from datetime import datetime, timedelta

from db_connector import get_db_connection, make_query
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
    query = ("""SELECT BIN_TO_UUID(id), email, name, password_hush"""
             """ FROM user WHERE email = %s""")
    results = make_query(query, (email,))
    stored_hush = results[3].encode()
    pass_match = bcrypt.checkpw(password.encode(), stored_hush)
    name = results[2]
    if pass_match:
        user_id = results[0]
        token = generate_web_token(user_id)
        return token, name, stored_hush
    else:
        return False, None, None


def generate_web_token(user_id):
    time_now = datetime.now()
    time_exp = time_now + timedelta(hours=2)
    time_now = time_now.strftime("%d.%m.%Y %H:%M:%S")
    time_exp = time_exp.strftime("%d.%m.%Y %H:%M:%S")
    payload_jwt = {'id': user_id, 'generated': time_now, 'exp': time_exp}
    token = jwt.encode(payload_jwt, JWT_SECRET_KEY, JWT_ALGORITHM)
    return token


def get_user_id(email):
    query = """SELECT BIN_TO_UUID(id) FROM user WHERE email = %s"""
    results = make_query(query, (email,))
    return results[0]
