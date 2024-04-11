#!/usr/bin/env python3
"""
Provides functionalities to encrypt passwords securly
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password securly using bcrypt
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against its hashed version
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    