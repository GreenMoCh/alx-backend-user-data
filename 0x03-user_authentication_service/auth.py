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
