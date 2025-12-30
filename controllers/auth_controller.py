import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from config import JWT_SECRET_KEY, JWT_ALGORITHM
from models.role_model import Role


class AuthService:
    def __init__(self):
        self.roles = Role.get_roles_from_db()

    @staticmethod
    def get_role_from_token(token):
        pass

    @staticmethod
    def is_jwt_valid(token):
        try:
            jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return True
        except ExpiredSignatureError:
            return False
        except InvalidTokenError:
            return False
