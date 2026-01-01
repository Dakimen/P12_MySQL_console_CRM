import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
import json
import bcrypt

from config import JWT_SECRET_KEY, JWT_ALGORITHM
from models.role_model import Role


class AuthService:
    def __init__(self):
        self.roles = Role.get_roles_from_db()

    def get_roles_from_token(self, token):
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        roles = [role for role in payload.get('roles')]
        return roles

    @staticmethod
    def get_user_id_from_token(token):
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload.get('id')

    @staticmethod
    def is_jwt_valid(token):
        try:
            jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return True
        except ExpiredSignatureError:
            return False
        except InvalidTokenError:
            return False

    @staticmethod
    def write_token_to_temp(token):
        data = {
            "token": token
        }
        file_path = 'temp.json'
        with open(file_path, 'w') as temp_storage:
            json.dump(data, temp_storage, indent=4)
        return None

    @staticmethod
    def check_password(password, stored_hush):
        return bcrypt.checkpw(password.encode(), stored_hush.encode())


def generate_web_token(user_id, roles):
    time_now = datetime.now(timezone.utc)
    time_exp = time_now + timedelta(hours=2)
    payload_jwt = {'id': user_id, 'roles': roles,
                   'iat': time_now, 'exp': time_exp}
    token = jwt.encode(payload_jwt, JWT_SECRET_KEY, JWT_ALGORITHM)
    return token
