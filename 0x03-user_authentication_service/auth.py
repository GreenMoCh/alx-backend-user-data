#!/usr/bin/env python3
"""
Auth module for handling user auth
"""
import bcrypt
import uuid
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hashes the input password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed

def _generate_uuid(self) -> str:
    """
    Generates a new UUID str
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class"""

    def __init__(self) -> None:
        """Initialize Auth class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError
        except:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email=email, hashed_password=hashed_password)

            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check if the provided email and pwd valid
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hased_password)
        except:
            return False

    def create_session(self, email: str) -> str:
        """
        Create a session for the user and return the session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate.uuid()
            user.session_id = session_id
            self._db._session.commit()

            return session_id
        except:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        GEt user corresponding to the session ID
        """
        try:
            if session_id is None:
                return None

            user = self._db.find_user_by(session_id=session_id)
            return user
        except:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session for the user
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
        except:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Get reset password token
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError
        reset_token = str(uuid.uuid4())
        user.reset_token = reset_token
        self._db.commit()
        return reset_token

    def update_password(self, reset_token, password):
        """
        Updates password using reset_token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except:
            raise ValueError

        hashed_password = self._hash_password(password)

        user.hased_password = hashed_password
        user.reset_token = None

        self._db._session.commit()
        