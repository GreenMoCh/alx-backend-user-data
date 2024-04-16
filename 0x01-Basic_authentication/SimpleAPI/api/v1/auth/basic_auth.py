#!/usr/bin/env python3
"""
Basic Authentification
"""
import base64
from .auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Implements extract basic_auth
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts base64_authorization_header
        """
        if authorization_header is None:
            return None
        
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ")[-1]


    def decode_base64_authorozation_header(self, base64_authorization_header: str) -> str:
        """
        Decode base64_authorozation_header
        """
        if  base64_authorization_header is None:
            return None
        
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode = base64_authorization_header.encode('utf-8')
            decode = base64.b64decode(decode)
            return decode.decode('utf-8')
        except Exception:
            return None


    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> str:
        """
        Extracts user_credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header[len(email) + 1:]

        return (email, password)


    def user_object_from_creentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns user's instance
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None


    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns user's instance
        """
        Auth_header = self.authorized_header(request)
        if Auth_header is not None:
            token = self.extract_base64_authorization_header(Auth_header)
            if token is not None:
                decoded = self.decode_base64_authorozation_header(token)
                if decoded is not None:
                    email, pwd = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_creentials(email, pwd)
        
        return
