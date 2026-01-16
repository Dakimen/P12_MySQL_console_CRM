import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta, timezone
import json
import bcrypt
import sys

from config import JWT_SECRET_KEY, JWT_ALGORITHM
from views.auth_view import token_expired_notification


class AuthService:
    """
    Service class responsible for authentication- and authorization-related
    operations such as JWT handling, role extraction, password verification,
    and temporary token storage.
    """

    @staticmethod
    def get_roles(token):
        """
        Decode a JWT and extract the user's roles.

        Args:
            token (str): A JSON Web Token containing a 'roles' claim.

        Returns:
            list: A list of roles extracted from the token payload.

        Raises:
            jwt.ExpiredSignatureError: If the token has expired.
            jwt.InvalidTokenError: If the token is invalid.
        """
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        roles = [role for role in payload.get('roles')]
        return roles

    @staticmethod
    def clean_json_temp(temp_storage):
        """
        Clear the contents of a temporary JSON file by overwriting it
        with an empty JSON object.

        Args:
            temp_storage (str): Path to the temporary JSON file.

        Returns:
            None
        """
        with open(temp_storage, 'w') as file:
            json.dump({}, file)

    def logout(self, temp_storage="temp.json"):
        """
        Performs logout by clearing the contents of a temporary JSON file
        and exiting program.

        Args:
            temp_storage (str): Path to the temporary JSON file.

        Returns:
            None, exits program
        """
        self.clean_json_temp(temp_storage)
        return sys.exit()

    @staticmethod
    def get_user_id_from_token(token):
        """
        Decode a JWT and extract the user ID.

        Args:
            token (str): A JSON Web Token containing an 'id' claim.

        Returns:
            int | str | None: The user ID from the token payload,
            or None if the claim is missing.

        Raises:
            jwt.ExpiredSignatureError: If the token has expired.
            jwt.InvalidTokenError: If the token is invalid.
        """
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload.get('id')

    @staticmethod
    def get_user_id():
        """
        Retrieve the user ID from a valid JWT stored in the temporary file.

        This method:
        1. Reads the token from temporary storage
        2. Validates the token
        3. Extracts and returns the user ID

        If the token is invalid or expired, a notification is triggered
        and the application exits.

        Returns:
            int | str: The authenticated user's ID.

        Side Effects:
            - Calls `token_expired_notification()`
            - Terminates the program using `sys.exit()` if the token is invalid
        """
        token = AuthService.get_token_from_temp()
        permission = AuthService.is_jwt_valid(token)
        if permission is True:
            user_id = AuthService.get_user_id_from_token(token)
            return user_id
        else:
            token_expired_notification()
            sys.exit()

    @staticmethod
    def is_jwt_valid(token):
        """
        Validate a JSON Web Token.

        Args:
            token (str | None): The JWT to validate.

        Returns:
            bool: True if the token is valid and not expired,
            False otherwise.
        """
        if token is not None:
            try:
                jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
                return True
            except ExpiredSignatureError:
                return False
            except InvalidTokenError:
                return False
        else:
            return False

    @staticmethod
    def write_token_to_temp(token):
        """
        Write a JWT to a temporary JSON file for later retrieval.

        Args:
            token (str): The JSON Web Token to store.

        Returns:
            None

        Side Effects:
            - Creates or overwrites 'temp.json' in the current directory.
        """
        data = {
            "token": token
        }
        file_path = 'temp.json'
        with open(file_path, 'w') as temp_storage:
            json.dump(data, temp_storage, indent=4)
        return None

    @staticmethod
    def check_password(password, stored_hush):
        """
        Verify a plaintext password against a stored bcrypt hash.

        Args:
            password (str): The plaintext password provided by the user.
            stored_hush (str): The bcrypt-hashed password stored in the db.

        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        try:
            return bcrypt.checkpw(password.encode(), stored_hush.encode())
        except ValueError:
            return False

    @staticmethod
    def generate_web_token(user_id, roles):
        """
        Generate a JSON Web Token for a user.

        The token includes:
        - User ID
        - User roles
        - Issued-at timestamp
        - Expiration timestamp (2 hours)

        Args:
            user_id (int | str): The unique identifier of the user.
            roles (list): A list of roles assigned to the user.

        Returns:
            str: A signed JSON Web Token.
        """
        time_now = datetime.now(timezone.utc)
        time_exp = time_now + timedelta(hours=2)
        payload_jwt = {'id': user_id, 'roles': roles,
                       'iat': time_now, 'exp': time_exp}
        token = jwt.encode(payload_jwt, JWT_SECRET_KEY, JWT_ALGORITHM)
        return token

    @staticmethod
    def get_token_from_temp():
        """
        Retrieve a JWT from the temporary JSON file.

        Returns:
            str | None: The stored JSON Web Token if available,
            otherwise None.

        Handles:
            - File not found
            - Missing token key
            - Invalid or empty JSON content
        """
        try:
            with open("temp.json", 'r') as file:
                data = json.load(file)
                token = data['token']
            return token
        except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
            return None
